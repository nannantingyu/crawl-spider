# -*- coding: utf-8 -*-
from Controller import Controller
from model.crawl_image_map import CrawlImageMap

class FiledownController(Controller):
    def __init__(self, topic="downfile_queue_with_thumb"):
        super(FiledownController, self).__init__(topic, 'filedown')

    def run(self):
        for message in self.consumer:
            if message is not None:
                file = message.value
                if file is None:
                    continue

                fileinfo = file.split('_____')
                file_url = fileinfo[0]
                file_save_path = fileinfo[1]

                print file_save_path, "____", file_url
                image_map = CrawlImageMap(img_path=file_save_path, real_path=file_url)
                try:
                    with self.session_scope(self.sess) as session:
                        query = session.query(CrawlImageMap.id).filter(
                            CrawlImageMap.img_path == file_save_path
                        ).one_or_none()

                        if query is None:
                            session.add(image_map)
                except Exception,e:
                    self.logger.error('Catch an exception.', exc_info=True)