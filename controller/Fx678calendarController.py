# -*- coding: utf-8 -*-
from model.crawl_article import CrawlArticle
from model.crawl_fx678_economic_calendar import CrawlFx678EconomicCalendar
from model.crawl_fx678_economic_event import CrawlFx678EconomicEvent
from model.crawl_fx678_economic_holiday import CrawlFx678EconomicHoliday
from Controller import Controller
import json

class Fx678calendarController(Controller):
    def __init__(self, topic="crawl_fx678_calendar"):
        super(Fx678calendarController, self).__init__(topic, 'fx678_calendar')
        self.type_model_map = {
            "calendar": CrawlFx678EconomicCalendar,
            "event": CrawlFx678EconomicEvent,
            "holiday": CrawlFx678EconomicHoliday
        }

    def run(self):
        for msg in self.consumer:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                dtype= data['dtype'] if "dtype" in data else "calendar"

                del data['dtype']
                self.handle_data(dtype, data)

            except Exception, e:
                self.logger.error('Catch an exception.', exc_info=True)


    def handle_data(self, dtype, data):
        with self.session_scope(self.sess) as session:
            try:
                model = self.type_model_map[dtype]
                model_obj = model(**data)
                query = session.query(model.id).filter(
                    model.source_id == model_obj.source_id
                ).one_or_none()

                if query is None:
                    session.add(model_obj)
                    session.flush()

                    data['id'] = model_obj.id
                    data['dtype'] = "insert"
                    data['source_site'] = "fx678"
                    self.hook_data(data, data_formatter=dtype)
                else:
                    session.query(model).filter(
                        model.id == query[0]
                    ).update(data)

                    data['id'] = query[0]
                    data['dtype'] = "update"
                    data['source_site'] = "fx678"
                    self.hook_data(data, data_formatter=dtype)
            except Exception,e:
                session.rollback()