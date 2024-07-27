import os
import yt_dlp  # Import the yt_dlp module for downloading videos

# Function to list available formats for a given URL
def list_formats(url):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)  # Extract info without downloading
        formats = info_dict.get('formats', None)  # Get the available formats
        if formats:
            print("Available formats:")
            for f in formats:
                # Safely access the keys to avoid KeyError
                itag = f.get('itag', 'N/A')
                resolution = f.get('resolution', 'N/A')
                fps = f.get('fps', 'N/A')
                mime_type = f.get('mime_type', 'N/A')
                print(f"itag: {itag}, resolution: {resolution}, fps: {fps}, type: {mime_type}")
        else:
            print("No formats found.")

# Function to download media (audio or video) from YouTube
def download_media(url, download_type):
    # Set the directory where downloaded files will be saved
    output_path = 'D:/downloads'
    
    # Create the directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Set download options based on whether the user wants audio or video
    if download_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',  # Download the best audio available
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Save with video title
        }
    else:  # If the user wants video
        ydl_opts = {
            'format': 'best[ext=mp4]',  # Download the best combined audio and video available in mp4 format
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Save with video title
        }

    # Try to download the media
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # Create a yt_dlp object with the options
            info_dict = ydl.extract_info(url, download=True)  # Extract and download the media
            file_path = ydl.prepare_filename(info_dict)  # Prepare the filename
            return info_dict.get('title', 'Unknown Title'), file_path  # Return the title and file path
    except Exception as e:
        print(f"Error: {e}")  # Print any error that occurs
        return None, None  # Return None if there's an error

# Main program execution
if __name__ == '__main__':
    # Get the YouTube URL from the user
    url = input("Enter the YouTube URL: ")
    
    # List available formats for the given URL
    list_formats(url)
    
    # Get the type of download (audio or video) from the user
    download_type = input("Do you want to download 'audio' or 'video'? ").lower()

    # Call the download function and get the title and filename
    title, filename = download_media(url, download_type)
    
    # Check if the download was successful and provide feedback to the user
    if title and filename:
        print(f'Download complete: {title}')  # Print the title of the downloaded media
        print(f'File saved as: {filename}')  # Print the path where the file is saved
    else:
        print("An error occurred during the download. Please check the URL and try again.")  # Error message
