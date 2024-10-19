import gridfs
from pytubefix.extract import video_id

import mongodb_controller
from db_manager.models import Orders
from db_manager.mongodb_controller import get_mongo_database

import model_controller

class VideoController:
    def __init__(self):
        self.mongodb_ref = get_mongo_database("videos")


    def store_video_to_mongodb(self, file_path):
        db = self.mongodb_ref
        fs = gridfs.GridFS(db)

        with open(file_path, "rb") as f:
            video_ref_id = fs.put(f, filename=file_path.split("/")[-1])

        return video_ref_id


    def store_video(self, video_file_path, order_id):
        video_ref_id = self.store_video_to_mongodb(video_file_path)

        try:
            request_order = Orders.objects.get(id=order_id)
        except Orders.DoesNotExist:
            raise ValueError(f"Order with ID {order_id} does not exist.")

        gv_controller = model_controller.ModelController("GeneratedVideos")
        generated_video = gv_controller.add(user=request_order.user,video_ref_id=video_ref_id)

        return generated_video

    def retrieve_video(self, video_ref_id):
        db = self.mongodb_ref
        fs = gridfs.GridFS(db)

        return fs.get(video_ref_id)

