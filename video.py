import requests
import aria2p
from datetime import datetime
import asyncio
import os
import logging

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=6800,
        secret=""
    )
)

async def download_video(url, reply_msg, user_mention, user_id):
    try:
        # Get video download link from API
        response = requests.get(f"https://pika-terabox-dl.vercel.app/?url={url}")
        response.raise_for_status()

        data = response.json()

        # Validate API response
        if not data.get("ok"):
            raise Exception("API response indicates failure")

        if "downloadLink" not in data or "filename" not in data:
            raise Exception("Invalid API response format: Missing 'downloadLink' or 'filename'")

        fast_download_link = data["downloadLink"]
        video_title = data["filename"]

        # Start download
        download = aria2.add_uris([fast_download_link])
        start_time = datetime.now()

        while not download.is_complete:
            download.update()
            percentage = download.progress
            done = download.completed_length
            total_size = download.total_length
            speed = download.download_speed
            eta = download.eta
            elapsed_time_seconds = (datetime.now() - start_time).total_seconds()

            progress_text = f"📥 **Downloading...**\n🎬 {video_title}\n🗂 **{done}/{total_size}**\n🚀 Speed: {speed} | ⏳ ETA: {eta}"
            await reply_msg.edit_text(progress_text)
            await asyncio.sleep(2)

        if download.is_complete:
            file_path = download.files[0].path
            await reply_msg.edit_text("✅ **Download Complete! Uploading...**")
            return file_path, video_title  # Return file path and title for upload function
        else:
            raise Exception("Download failed")

    except Exception as e:
        logging.error(f"Error in download_video: {e}")
        await reply_msg.edit_text("⚠️ Error downloading the video. Please try again later.")
        return None, None


async def upload_video(client, file_path, video_title, reply_msg, collection_channel_id, user_mention, user_id, message):
    try:
        file_size = os.path.getsize(file_path)
        uploaded = 0
        start_time = datetime.now()
        last_update_time = time.time()

        async def progress(current, total):
            nonlocal uploaded, last_update_time
            uploaded = current
            percentage = (current / total) * 100
            elapsed_time_seconds = (datetime.now() - start_time).total_seconds()

            if time.time() - last_update_time > 2:
                progress_text = f"🚀 **Uploading...**\n🎬 {video_title}\n🗂 **{uploaded}/{total}**\n⏳ ETA: {int((total - uploaded) / (uploaded / elapsed_time_seconds))}s"
                try:
                    await reply_msg.edit_text(progress_text)
                    last_update_time = time.time()
                except Exception as e:
                    logging.warning(f"Error updating progress message: {e}")

        with open(file_path, 'rb') as file:
            collection_message = await client.send_video(
                chat_id=collection_channel_id,
                video=file,
                caption=f"✨ {video_title}\n👤 ʟᴇᴇᴄʜᴇᴅ ʙʏ : {user_mention}\n📥 ᴜsᴇʀ ʟɪɴᴋ: tg://user?id={user_id}",
                progress=progress
            )

            await client.copy_message(
                chat_id=message.chat.id,
                from_chat_id=collection_channel_id,
                message_id=collection_message.id
            )

            await asyncio.sleep(1)
            await message.delete()
            await message.reply_sticker("CAACAgIAAxkBAAEZdwRmJhCNfFRnXwR_lVKU1L9F3qzbtAAC4gUAAj-VzApzZV-v3phk4DQE")

        await reply_msg.delete()
        os.remove(file_path)
        return collection_message.id

    except Exception as e:
        logging.error(f"Error in upload_video: {e}")
        await reply_msg.edit_text("⚠️ Error uploading the video. Please try again later.")
        return None
        
