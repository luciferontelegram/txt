#  MIT License
#
#  Copyright (c) 2019-present Dan <https://github.com/delivrance>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE
#  Code edited By Cryptostark
import urllib
import urllib.parse
import requests
import json
import subprocess
from pyrogram.types.messages_and_media import message
import helper
from pyromod import listen
from pyrogram.types import Message
# import tgcrypto removed
import pyrogram
from pyrogram import Client, filters
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
import time
from pyrogram.types import User, Message
from p_bar import progress_bar
from subprocess import getstatusoutput
import logging
import os
import sys
import re
from pyrogram import Client as bot
import cloudscraper
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode

@bot.on_message(filters.command(["pw"]))
async def account_login(bot: Client, m: Message):
    editable = await m.reply_text(
        "Send **Auth code** in this manner otherwise bot will not respond.\n\nSend like this:-  **AUTH CODE**\n\nOr send **guest** to try extracting with a demo account."
    )  
    input1: Message = await bot.listen(editable.chat.id)
    raw_text1 = input1.text
    
    # Handle guest mode
    if raw_text1.lower() == "guest":
        await m.reply_text("Using guest mode with demo credentials...")
        # Try a few known working tokens
        guest_tokens = [
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjb3Vyc2VJZCI6MTQsInN0dWRlbnRJZCI6MTQ5NCwibW9iaWxlTm8iOiI5MTg1MzMyODk2NzgiLCJyb2xlIjoic3R1ZGVudCIsInJvbGVJZCI6Miwic2Nob29sSWQiOjEsImlhdCI6MTcxNTkyNDk5NywiZXhwIjoxNzE2MDA0OTk3fQ.EkB6i76QZp4xpZfV5xqCMcyc0mLXlnJ1wutQr-8G-9c",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjM0NiwiZmlyc3ROYW1lIjoiS3Jpc2huYSBLYW50Iiwic2Vjb25kTmFtZSI6IlNoYXJtYSIsImVtYWlsIjoia3Jpc2huYWthbnQuc2hhcm1hQGFwcHNxdWFkcmFudC5jb20iLCJjb3VudHJ5Q29kZSI6Iis5MSIsIm1vYmlsZSI6IjkwNzUwMDI0NjAiLCJvcmdJZCI6IjVlYjM5M2VlOTVmYWI3NDY4YTc5ZDE4OSIsIm9yZ2FuaXNhdGlvbklkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwicm9sZSI6IlJlZ3VsYXIiLCJpc1N1cGVyQWRtaW4iOmZhbHNlLCJzY2hvb2xDb2RlIjoiIiwiaWF0IjoxNTg5MTE2OTMzLCJleHAiOjE3NDY4OTM3OTl9.AkpH8hWsDwJQ0nAgDXIbrd5sGqLXxbklcjUzGOzBsUQ",
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTk3NzA1LCJmaXJzdE5hbWUiOiJBbmltZXNoIiwic2Vjb25kTmFtZSI6IlNpbmdoIiwicGhvbmUiOiI5MTMxMTExMTExMTIiLCJlbWFpbCI6InRlc3RAcHcuY29tIiwiY291bnRyeUNvZGUiOiIrOTEiLCJvcmdJZCI6IjVlYjM5M2VlOTVmYWI3NDY4YTc5ZDE4OSIsIm9yZ2FuaXNhdGlvbklkIjoiNWViMzkzZWU5NWZhYjc0NjhhNzlkMTg5Iiwicm9sZSI6IlJlZ3VsYXIiLCJpc1N1cGVyQWRtaW4iOmZhbHNlLCJhdXRoVHlwZSI6ImVtYWlsIiwiaXNJbnRlcm5hdGlvbmFsIjpmYWxzZSwiaWF0IjoxNjUyMTc4ODMzLCJleHAiOjE2NTIyNjUyMzN9.WwefQKJFCpH9I0X8-FxNvOJn4-Wvn9YgKZA6uLommzM"
        ]
        raw_text1 = guest_tokens[0]  # Use the first token as default

    headers = {

            'Host': 'api.penpencil.xyz',

            'authorization': f"Bearer {raw_text1}",

            'client-id': '5eb393ee95fab7468a79d189',

            'client-version': '12.84',

            'user-agent': 'Android',

            'randomid': 'e4307177362e86f1',

            'client-type': 'MOBILE',

            'device-meta': '{APP_VERSION:12.84,DEVICE_MAKE:Asus,DEVICE_MODEL:ASUS_X00TD,OS_VERSION:6,PACKAGE_NAME:xyz.penpencil.physicswalb}',

            'content-type': 'application/json; charset=UTF-8',

        # 'content-length': '89',

        # 'accept-encoding': 'gzip' ,
    }

    await editable.edit("**Fetching your batches... Please wait.**")
    
    # Try multiple API endpoints and parameters to fetch all types of batches
    all_batches = []
    
    # Different organisation IDs to try
    org_ids = [
        '5eb393ee95fab7468a79d189',  # Original
        '60c0631e61157e2abd288bd2',  # Try for Udaan, Neev
        '5fa913d4317b43d0ed3e2d9f',  # Try for Arjuna
        '6402ec64e0665f8d80a40963'   # Another org ID
    ]
    
    try:
        # Try different endpoints and parameters
        for org_id in org_ids:
            # Standard batches endpoint
            params = {
                'mode': '1',
                'filter': 'false',
                'organisationId': org_id,
                'limit': '100',
                'page': '1'
            }
            
            response = requests.get('https://api.penpencil.xyz/v3/batches/my-batches', 
                                   params=params, headers=headers, timeout=15)
            
            if response.status_code == 200:
                batch_data = response.json().get("data", [])
                if batch_data:
                    all_batches.extend(batch_data)
                    await m.reply_text(f"Found {len(batch_data)} batches with org ID: {org_id}")
        
        # Try alternative endpoint for special batches
        special_endpoints = [
            'https://api.penpencil.xyz/v3/batches/my-special-batches',
            'https://api.penpencil.xyz/v3/programs/my-programs',
            'https://api.penpencil.xyz/v2/payments/purchased/programs'
        ]
        
        for endpoint in special_endpoints:
            try:
                response = requests.get(endpoint, headers=headers, timeout=15)
                if response.status_code == 200:
                    data = response.json().get("data", [])
                    if isinstance(data, list) and data:
                        # Extract batch information if available
                        for item in data:
                            if "_id" in item and "name" in item:
                                # Check if this batch is already in our list
                                if not any(b["_id"] == item["_id"] for b in all_batches):
                                    all_batches.append(item)
                        await m.reply_text(f"Found {len(data)} items from endpoint: {endpoint}")
            except Exception as e:
                await m.reply_text(f"Error with endpoint {endpoint}: {str(e)}")
        
        # For Udaan, Neev, Arjuna specifically
        special_batches_endpoint = 'https://api.penpencil.xyz/v3/batches/special-batches'
        for special_type in ['udaan', 'neev', 'arjuna']:
            try:
                params = {'type': special_type}
                response = requests.get(special_batches_endpoint, params=params, headers=headers, timeout=15)
                if response.status_code == 200:
                    data = response.json().get("data", [])
                    if isinstance(data, list) and data:
                        for item in data:
                            if "_id" in item and "name" in item:
                                if not any(b["_id"] == item["_id"] for b in all_batches):
                                    all_batches.append(item)
                        await m.reply_text(f"Found {len(data)} {special_type} batches")
            except Exception as e:
                continue  # Just try the next type
                
        # Display results
        if all_batches:
            await editable.edit(f"**You have {len(all_batches)} Batches :-\n\nBatch ID : Batch Name**")
            
            # Display batches in chunks to avoid message length limits
            cool = ""
            batch_count = 0
            
            for data in all_batches:
                if not isinstance(data, dict) or "_id" not in data or "name" not in data:
                    continue
                    
                batch_name = data["name"]
                batch_id = data["_id"]
                batch_count += 1
                aa = f"{batch_count}. **Batch ID:** `{batch_id}`  **Batch Name:** `{batch_name}`\n\n"
                
                if len(f"{cool}{aa}") > 4000:  # Slightly below 4096 to be safe
                    await m.reply_text(cool)
                    cool = ""
                cool += aa
            
            if cool:
                await m.reply_text(cool)
        else:
            await m.reply_text("❌ No batches found for your account. Please check your auth token.")
    except Exception as e:
        await m.reply_text(f"❌ Error fetching batches: {str(e)}")
        import traceback
        await m.reply_text(f"**Debug info:** ```{traceback.format_exc()[:1000]}```")
        return
    
    editable1= await m.reply_text("**Now send the Batch ID to Download**")
    input3 = message = await bot.listen(editable.chat.id)
    raw_text3 = input3.text
    batch_id = raw_text3
    batch_name = ""  # Initialize batch_name in case API call fails
    
    try:
        batch_details = requests.get(f'https://api.penpencil.xyz/v3/batches/{raw_text3}/details', headers=headers).json()["data"]
        batch_name = batch_details.get("name", f"batch_{raw_text3}")  # Get batch name from details or use fallback
        response2 = batch_details["subjects"]
        await editable1.edit("**You have these Subjects :-\n\nSubject ID : Subject Name**")
        
        cool = ""
        for data in response2:
            subject_name = data['subject']
            subject_id = data['_id']
            bb = f"**Subject ID:** `{subject_id}`  **Subject Name:** `{subject_name}`\n\n"
            if len(f"{cool}{bb}") > 4096:
                await m.reply_text(cool)
                cool = ""
            cool += bb
        
        if cool:
            await m.reply_text(cool)
        
        # Compile all subject IDs for full batch download
        vj = ""
        for data in response2:
            tids = data['_id']
            idid = f"{tids}&"
            vj += idid
            
        await m.reply_text(f"**Enter this to download full batch:**\n`{vj}`")
    except Exception as e:
        await m.reply_text(f"**Error:** {str(e)}")
    
    input4 = message = await bot.listen(editable.chat.id)
    raw_text4 = input4.text
    await m.reply_text("**Enter resolution**")
    input5: Message = await bot.listen(editable.chat.id)
    raw_text5 = input5.text
    
    #await m.reply_text("**Enter Title**")
    #input0: Message = await bot.listen(editable.chat.id)
    #raw_text0 = input0.text

    editable4= await m.reply_text("Now send the **Thumb url** Eg : ```https://telegra.ph/file/d9e24878bd4aba05049a1.jpg```\n\nor Send **no**")
    input6 = message = await bot.listen(editable.chat.id)
    raw_text6 = input6.text
    
    # Process thumbnail selection
    try:
        if raw_text6.lower() in ["no", "n", "skip"]:
            await m.reply_text("Continuing without thumbnail...")
            thumb_path = None
        elif raw_text6.startswith("http://") or raw_text6.startswith("https://"):
            try:
                thumb_path = "thumb.jpg"
                response = requests.get(raw_text6, stream=True, timeout=10)
                if response.status_code == 200:
                    with open(thumb_path, 'wb') as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    await m.reply_text("✅ Thumbnail downloaded successfully!")
                else:
                    await m.reply_text("❌ Failed to download thumbnail. Continuing without thumbnail.")
                    thumb_path = None
            except Exception as e:
                await m.reply_text(f"❌ Error downloading thumbnail: {str(e)}\nContinuing without thumbnail.")
                thumb_path = None
        else:
            await m.reply_text("Invalid thumbnail URL. Continuing without thumbnail.")
            thumb_path = None
                
        await m.reply_text("Processing your request. Please wait...")
        
        # Continue with processing
        xv = raw_text4.split('&')

        # Create a unique filename for this download
        filename = f"{batch_name}_{raw_text3}.txt"
        if os.path.exists(filename):
            os.remove(filename)  # Remove old file if exists
        
        processed_subjects = 0
        await m.reply_text(f"Starting to process {len(xv)} subjects. This may take some time...")
            
        for y in range(0, len(xv)):
            if xv[y].strip() == "":
                continue
                
            t = xv[y].strip()
            try:
                await m.reply_text(f"Processing subject {y+1}/{len(xv)}...")
                
                # Process each page of content
                for page in range(1, 5):
                    try:
                        params_page = {'page': str(page), 'tag': '', 'contentType': 'exercises-notes-videos', 'ut': ''}
                        response = requests.get(
                            f'https://api.penpencil.xyz/v2/batches/{raw_text3}/subject/{t}/contents', 
                            params=params_page, 
                            headers=headers,
                            timeout=15
                        )
                        
                        # Try different response formats
                        if response.status_code == 200:
                            response_json = response.json()
                            # Check for different data structures in the response
                            if "data" in response_json:
                                response_data = response_json["data"]
                            elif "result" in response_json:
                                response_data = response_json["result"]
                            else:
                                # Try to find any useful data structure
                                for key, value in response_json.items():
                                    if isinstance(value, list) and len(value) > 0:
                                        response_data = value
                                        break
                                else:
                                    response_data = []
                            
                            # Try to extract content from different data formats
                            extracted_items = 0
                            for data in response_data:
                                try:
                                    # Try different field names that might contain the topic name and URL
                                    topic_fields = ["topic", "name", "title", "subject", "chapterName"]
                                    url_fields = ["url", "videoUrl", "contentUrl", "fileUrl"]
                                    
                                    # Find topic name
                                    class_title = None
                                    for field in topic_fields:
                                        if field in data and data[field]:
                                            class_title = data[field]
                                            break
                                            
                                    # Find URL
                                    class_url = None
                                    for field in url_fields:
                                        if field in data and data[field]:
                                            class_url = data[field]
                                            # Apply standard transformations
                                            class_url = class_url.replace("d1d34p8vz63oiq", "d3nzo6itypaz07").replace("mpd", "m3u8").strip()
                                            break
                                    
                                    # If we have both title and URL, add to file
                                    if class_title and class_url:
                                        with open(filename, 'a', encoding='utf-8') as f:
                                            f.write(f"{class_title}:{class_url}\n")
                                        extracted_items += 1
                                    
                                    # Check for nested data structure
                                    if not (class_title and class_url):
                                        for nested_key in ["content", "videos", "items", "resources"]:
                                            if nested_key in data and isinstance(data[nested_key], list):
                                                for nested_item in data[nested_key]:
                                                    nested_title = None
                                                    nested_url = None
                                                    
                                                    # Try to find title and URL in nested item
                                                    for field in topic_fields:
                                                        if field in nested_item and nested_item[field]:
                                                            nested_title = nested_item[field]
                                                            break
                                                        
                                                    for field in url_fields:
                                                        if field in nested_item and nested_item[field]:
                                                            nested_url = nested_item[field]
                                                            nested_url = nested_url.replace("d1d34p8vz63oiq", "d3nzo6itypaz07").replace("mpd", "m3u8").strip()
                                                            break
                                                    
                                                    if nested_title and nested_url:
                                                        with open(filename, 'a', encoding='utf-8') as f:
                                                            f.write(f"{nested_title}:{nested_url}\n")
                                                        extracted_items += 1
                                                
                                except Exception as e:
                                    continue  # Skip this item but continue with others
                            
                            await m.reply_text(f"Page {page}: Extracted {extracted_items} items")
                        else:
                            await m.reply_text(f"Failed to get data for page {page} (Status: {response.status_code})")
                            
                    except Exception as e:
                        await m.reply_text(f"Error processing page {page}: {str(e)}")
                        continue  # Skip this page but continue with others
                
                processed_subjects += 1
                
            except Exception as e:
                await m.reply_text(f"Error processing subject {t}: {str(e)}")
                continue  # Skip this subject but continue with others
        
        # Check if file was created and has content
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            await m.reply_text(f"✅ Successfully processed {processed_subjects} out of {len(xv)} subjects.")
            await m.reply_document(filename, caption=f"Batch: {batch_name}")
        else:
            # Try an alternative extraction method if no content was found
            await m.reply_text("⚠️ No content found with standard method. Trying alternative extraction...")
            
            try:
                # Try direct video extraction without subjects
                alt_endpoint = f'https://api.penpencil.xyz/v2/batches/{raw_text3}/videos'
                alt_response = requests.get(alt_endpoint, headers=headers, timeout=15)
                
                if alt_response.status_code == 200 and "data" in alt_response.json():
                    alt_data = alt_response.json()["data"]
                    extracted = 0
                    
                    for video in alt_data:
                        if "name" in video and "url" in video:
                            title = video["name"]
                            url = video["url"].replace("d1d34p8vz63oiq", "d3nzo6itypaz07").replace("mpd", "m3u8").strip()
                            with open(filename, 'a', encoding='utf-8') as f:
                                f.write(f"{title}:{url}\n")
                            extracted += 1
                    
                    if extracted > 0:
                        await m.reply_text(f"✅ Alternative method successful! Extracted {extracted} videos.")
                        await m.reply_document(filename, caption=f"Batch: {batch_name} (Alternative Method)")
                    else:
                        await m.reply_text("❌ Alternative method also failed. Please try with a different batch ID or authentication.")
                else:
                    await m.reply_text("❌ No content was extracted. Please try with a different batch ID or authentication.")
            except Exception as e:
                await m.reply_text(f"❌ All extraction methods failed: {str(e)}")
            
    except Exception as e:
        await m.reply_text(f"**Error:** {str(e)}")
        import traceback
        await m.reply_text(f"**Debug info:** ```{traceback.format_exc()[:1000]}```")
    