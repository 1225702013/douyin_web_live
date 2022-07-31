import traceback
from datetime import datetime
from store.mongo import MongoStore
from config.helper import config
from scripts import globalVar

class Base:

    instance = None

    def set_payload(self, payload):
        self.instance.ParseFromString(payload)

    def extra_info(self):
        return dict()
        
    def user(self):
        if(hasattr(self.instance, 'user')):
            return self.instance.user
        
        return None

    def persists(self, message_type=""):
        user = self.user()
        d = {
            'id': str(user.id),
            'shortId': str(user.shortId),
            'nickname': user.nickname,
            'gender': str(user.gender),
            "roomId": str(self.instance.common.roomId),
            'content': self.format_content(),
            "type": message_type,
            "payGradeLevel": user.badgeImageList.content.level,
            "alternativeText":  user.badgeImageList.content.alternativeText,
            "followingCount": str(user.followInfo.followingCount),
            "followerCount": str(user.followInfo.followingCount)
        }
        globalVar.get_value("queue").put(d)
        if config()['mongo']['enabled'] != 'on':
            return

        try:
            store = MongoStore()

            user = self.user()
            if user is not None:
                store.set_collection('user')

                if not store.exists({'id': user.id}):
                    store.insert_one({
                        'id': user.id,
                        'shortId': user.shortId,
                        'nickname': user.nickname,
                        'gender': user.gender
                    })

            store.set_collection(self.instance.common.method)
            msg = {
                "msgId": self.instance.common.msgId,
                "roomId": self.instance.common.roomId,
                'content': self.format_content(),
                'created_at': datetime.today().replace(microsecond=0)
            }

            if user is not None:
                msg.update({
                    'userId': user.id
                })

            if len(self.extra_info()):
                msg.update(self.extra_info())

            store.insert_one(msg)
        except Exception as e:
            print(self.instance.common.method + ' persists error')
            print(traceback.format_exc())
        finally:
            store.close()

    def __str__(self):
        pass

