# -*- coding: utf-8 -*-
from model.crawl_economic_calendar import CrawlEconomicCalendar
from model.crawl_economic_event import CrawlEconomicEvent
from model.crawl_economic_holiday import CrawlEconomicHoliday
from Controller import Controller
import json, datetime

class Jin10calendarController(Controller):
    def __init__(self, topic="crawl_jin10_calendar"):
        super(Jin10calendarController, self).__init__(topic, 'jin10_calendar')
        self.type_model_map = {
            "calendar": CrawlEconomicCalendar,
            "event": CrawlEconomicEvent,
            "holiday": CrawlEconomicHoliday
        }

        self.key_map = {
            'pub_time': 'publish_time'
        }

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                dtype= data['dtype'] if "dtype" in data else "calendar"
                del data['dtype']

                data = self.key_replace(data)
                self.handle_data(dtype, data)
            except Exception, e:
                self.logger.error('Catch an exception.', exc_info=True)


    def handle_data(self, dtype, data):
        with self.session_scope(self.sess) as session:
            model = self.type_model_map[dtype]
            model_obj = model(**data)
            query = session.query(model.id).filter(
                model.source_id == model_obj.source_id
            ).one_or_none()

            if query is None:
                session.add(model_obj)
                session.flush()
            else:
                session.query(model).filter(
                    model.id == query[0]
                ).update(data)

            if dtype == 'calendar':
                self.hook_data('calendar/%s' % datetime.datetime.strptime(model_obj.publish_time, "%Y-%m-%d %H:%I:%S").strftime("%Y-%m-%d"))