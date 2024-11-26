import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from firebase_admin import messaging
from google.cloud.firestore_v1 import SERVER_TIMESTAMP
import time

import smhome_constants


cred = credentials.Certificate("sm-home-firebase-sdk.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': smhome_constants.DATABASE_URL
})


db_firestore = firestore.client()
def get_all_tokens():
    try:
        tokens_ref = db_firestore.collection_group(smhome_constants.ROOT_SM_HOME_NOTIFICATION)
        tokens = tokens_ref.stream()

        tokenUsers = []
        for token in tokens:
            token_data = token.to_dict()
            token_id = token.id
            tokenUsers.append({
                "token" : token_data['token'] , 
                "id" : token.id
            })

        seen_tokens = set()  # Tập hợp để theo dõi các token đã gặp
        unique_list = []     # Danh sách kết quả

        for item in tokenUsers:
            if item["token"] not in seen_tokens:
                seen_tokens.add(item["token"])
                unique_list.append(item)

        if len(unique_list) > 0 and unique_list[0] : 
            doc_ref = db.collection(smhome_constants.ROOT_SM_HOME_NOTIFICATION).document(unique_list[0]["id"])
            doc_ref.delete()
    
        return unique_list
    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")
        return []

# Gọi hàm và in dữ liệu
tokens_data = get_all_tokens()
# tokens_data = [1]
print(tokens_data)

tokenC = "eBIJswdyDstubmsntW5kY6:APA91bHChG3c6OCR9Kw6KtpTeYxKTpUg1F-T2WelIu8VupW-OkVrQnGBx4ibkmnl8FM2H3ETcNm4QaSHfCxWMwOjHulenLZyz1QbAV7Qvl8wNVSruI4pzuo"
def send_message_to_tokens(tokens, title, body):
    try : 
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=tokenC
        )

        # Gửi thông báo
        response = messaging.send(message)
        print(f"Response: {response}")
    except Exception as e : 
        tokens_ref = db_firestore.collection_group(smhome_constants.ROOT_SM_HOME_NOTIFICATION)
        print(f"Error: {e}")
                
# print(tokens_data)

# send_message_to_tokens(1, "Báo động", "Có người di chuyển")