from mongoengine import *


class HealthCareSpecialist(Document):
        image = StringField(max_length=100, required=True)
        name = StringField(max_length=100, required=True)
        specialized = StringField(max_length=100, required=True)
        phone = StringField(max_length=100, required=True)
        area = StringField(max_length=100, required=True)
        certification_experience = StringField(max_length=400)
        charge = IntField()

class HealthCareSpecialist_comment(Document):
	hc_specialist_phone = StringField(max_length=100)
	user_phone = StringField(max_length=100)
	user_name = StringField(max_length=100)
	comment = StringField(max_length=100)

class Message(Document):
    user_phone = StringField(max_length=100)
    advisor_phone = StringField(max_length=100)
    message_sender = StringField(max_length=100)
    message = StringField(max_length=100)
  

class HealthCareSpecialistDb():
    def __init__(self):
        pass   

    def add_health_care_specialist(self, image, name, specialized, phone, area, certification_experience, charge):
        #print(phone)
        hc_specialist = HealthCareSpecialist.objects(phone = phone )
        
        if hc_specialist:
            return {"success": True}
        else:
            new_hc_specialist = HealthCareSpecialist(image=image, name=name, specialized=specialized, phone=str(phone), area=area, certification_experience=certification_experience,charge=charge)
            new_hc_specialist.save()
            recent_added_hc_specialist = HealthCareSpecialist.objects(phone = phone )
            if recent_added_hc_specialist:
                return {"success": True}
            else:
                return {"success": False}



    def get_all_hc_specialist(self):
        hc_specialists = HealthCareSpecialist.objects()
        list_hc_specialist = []
        if len(hc_specialists) > 0:                                 			                                            
            for hc_specialist in hc_specialists:                             
                hc_specialist_dict = {                              
                   '_id': str(hc_specialist.pk),
                   'image': hc_specialist.image,
                   'name': hc_specialist.name,
                   'specialized': hc_specialist.specialized,
                   'phone': hc_specialist.phone,
                   'area': hc_specialist.area,
                   'certification_experience': hc_specialist.certification_experience,
                   'charge': hc_specialist.charge
                }
                list_hc_specialist.append(hc_specialist_dict)
        return list_hc_specialist	            
                  
    def get_single_hc_specialist(self, phone):
        hc_specialists = HealthCareSpecialist.objects(phone = phone)
        hc_specialist_info = [] 
        if hc_specialists:
            hc_specialist = hc_specialists[0]
            hc_specialist_Dict = {                              
                   '_id': str(hc_specialist.pk),
                   'image': hc_specialist.image,
                   'name': hc_specialist.name,
                   'specialized': hc_specialist.specialized,
                   'phone': hc_specialist.phone,
                   'area': hc_specialist.area,
                   'certification_experience': hc_specialist.certification_experience,
                   'charge': hc_specialist.charge
            }
            hc_specialist_info.append(hc_specialist_Dict)
        return hc_specialist_info


    def add_comment(self, hc_specialist_phone, user_phone, user_name, comment): 
        hc_specialist_comment = HealthCareSpecialist_comment(hc_specialist_phone=hc_specialist_phone, user_phone=user_phone, user_name=user_name, comment=comment)
        hc_specialist_comment.save()
        return {"success": True}


    def get_all_hc_specialist_comments(self, hc_specialist_phone):
        comments = HealthCareSpecialist_comment.objects( hc_specialist_phone = hc_specialist_phone )
        commentList = []
        if len(comments) > 0:                                 			                                            
            for hc_specialist_comment in comments:
                commentDict = {                              
				   '_id': str(hc_specialist_comment.pk),
				   'hc_specialist_phone': hc_specialist_comment.hc_specialist_phone,
				   'user_phone': hc_specialist_comment.user_phone,
				   'user_name': hc_specialist_comment.user_name,
				   'comment': hc_specialist_comment.comment
				}
                commentList.append(commentDict)
        return commentList  


    def delete_commnet(self, comment_pk):    
        comments = HealthCareSpecialist_comment.objects( pk = comment_pk ) 
        comment = comments.get( pk = comment_pk )    

        if len(comment) > 0:
            comment.delete()
            return {"success": True}
        else:
            return {"success": False}


    def add_messages(self, user_phone, advisor_phone, message_sender, message):
        #print(phone)
        message = Message.objects(user_phone=user_phone, advisor_phone=advisor_phone, message_sender=message_sender, message=message )
        message.save()

        recent_added_message = Message.objects(user_phone=user_phone, advisor_phone=advisor_phone, message_sender=message_sender, message=message )
        if recent_added_message:
            return {"success": True}
        else:
            return {"success": False}


    def get_all_user_advisor_messages(self, user_phone, advisor_phone):
        messages = Message.objects( user_phone=user_phone, advisor_phone=advisor_phone )
        message_list = []
        if len(messages) > 0:                                 			                                            
            for message in messages:
                messagetDict = {                              
				   '_id': str(message.pk),
				   'user_phone': message.user_phone,
				   'advisor_phone': message.advisor_phone,
				   'message_sender': message.message_sender,
				   'message': message.message
				}
                message_list.append(messageDict)
        return message_list              
           
    
