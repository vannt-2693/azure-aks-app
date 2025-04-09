import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, PublicAccess

# --- Configuration ---
# Get information from environment variables - Best practice for managing secrets
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')

if not connect_str:
    raise ValueError("Environment variable AZURE_STORAGE_CONNECTION_STRING is not set.")
if not container_name:
    raise ValueError("Environment variable AZURE_STORAGE_CONTAINER_NAME is not set.")

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24) # Needed for flash messages

# --- Connect to Azure Blob Storage ---
try:
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
    # Optional: Create container if it doesn't exist (requires permissions)
    # try:
    #     container_client.create_container()
    #     # Set public access level if needed (only do this if you understand the risks)
    #     # container_client.set_container_access_policy(signed_identifiers={}, public_access=PublicAccess.Blob)
    # except Exception as e:
    #      print(f"Container '{container_name}' already exists or an error occurred: {e}")

except Exception as e:
    raise ConnectionError(f"Could not connect to Azure Storage: {e}")

# --- Routes ---
@app.route('/')
def index():
    """Display the list of images and the upload form"""
    image_urls = []
    try:
        blob_list = container_client.list_blobs()
        # --- Import thư viện cần thiết cho SAS ---
        from azure.storage.blob import generate_blob_sas, BlobSasPermissions
        from datetime import datetime, timedelta
        # -----------------------------------------

        for blob in blob_list:
            blob_client = container_client.get_blob_client(blob.name)

            # --- Bỏ comment phần này để tạo và dùng SAS token ---
            sas_token = generate_blob_sas(
                account_name=blob_service_client.account_name,
                container_name=container_name,
                blob_name=blob.name,
                # Lấy account key từ credential của service client
                account_key=blob_service_client.credential.account_key,
                permission=BlobSasPermissions(read=True), # Chỉ cấp quyền đọc
                expiry=datetime.utcnow() + timedelta(hours=1) # Token hết hạn sau 1 giờ
            )
            # Tạo URL đầy đủ với SAS token
            image_url_with_sas = f"{blob_client.url}?{sas_token}"
            image_urls.append(image_url_with_sas)
            # --- Kết thúc phần SAS token ---

            # --- Comment hoặc xóa dòng lấy URL trực tiếp nếu dùng SAS ---
            # image_urls.append(blob_client.url)
            # ------------------------------------------------------

    except Exception as e:
        flash(f"Error retrieving image list: {e}", "error")

    return render_template('index.html', image_urls=image_urls)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle the image upload process"""
    if 'file' not in request.files:
        flash('No file part selected', 'warning')
        return redirect(url_for('index'))

    file = request.files['file']

    if file.filename == '':
        flash('No file selected for upload', 'warning')
        return redirect(url_for('index'))

    if file:
        try:
            # Create a unique filename to avoid collisions
            # Keep the original file extension
            _, file_extension = os.path.splitext(file.filename)
            filename = str(uuid.uuid4()) + file_extension
            blob_client = container_client.get_blob_client(filename)

            print(f"Uploading blob: {filename}")
            # Upload the file stream to Azure Blob Storage
            # Set overwrite=True to replace if a blob with the same name somehow exists
            blob_client.upload_blob(file.stream, overwrite=True)
            print(f"Upload successful: {blob_client.url}")
            flash(f'File "{file.filename}" uploaded successfully as "{filename}"!', 'success')

        except Exception as e:
            print(f"Error during upload: {e}")
            flash(f"An error occurred while uploading the file: {e}", "error")

        return redirect(url_for('index'))

# --- Run the application ---
if __name__ == '__main__':
    # Run on port 5000 and listen on all available IP addresses (important for Docker)
    # Turn off debug=True in production
    app.run(host='0.0.0.0', port=5000, debug=True)
