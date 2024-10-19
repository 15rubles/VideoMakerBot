from django.test import TestCase
from django.utils import timezone
from db_manager.models import Users, Orders, GeneratedVideos, OrderTypesDBNames
from db_manager.video_controller import VideoController
from db_manager.model_controller import ModelController
from unittest.mock import patch, MagicMock

class VideoControllerTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.models_controller = ModelController('User')
        cls.User = cls.models_controller.add(username='test', password='password123')
        cls.Order = cls.models_controller.add(
            user=cls.User,
            order_type=OrderTypesDBNames.objects.get(pk=1),
            order_status="test",
            desired_video_quantity=1,
            uploaded_video_quantity=0
        )

    @patch('db_manager.video_controller.gridfs.GridFS')
    @patch('db_manager.video_controller.get_mongo_database')
    def test_store_video(self,mock_get_mongo_database, mock_gridfs):
        mock_db = MagicMock()
        mock_get_mongo_database.return_value = mock_db
        mock_fs = mock_gridfs.return_value

        mock_fs.put.return_value = 'mock_video_id'

        video_controller = VideoController()
        video_file_path = '/static/testdata/videos/test_video.mp4'

        generated_video = video_controller.store_video(video_file_path, self.Order.id)

        self.assertIsNotNone(generated_video)
        self.assertEqual(generated_video.user, self.user)
        self.assertEqual(generated_video.video_ref_id, 'mock_video_id')
        self.assertTrue(generated_video.is_uploaded)