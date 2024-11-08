from django_rq.utils import get_statistics
from prometheus_client.metrics_core import GaugeMetricFamily


class ComponentCollector(object):

    def collect(self):
        yield self.get_django_rq_workers_count()
        yield self.get_django_rq_job_count()

    @staticmethod
    def get_django_rq_workers_count():

        django_rq_workers_count = GaugeMetricFamily(
            "django_rq_workers_count",
            'Number of workers',
            labels=['queue']
        )
        django_rq_stats = get_statistics()
        if "queues" in django_rq_stats:
            queues = django_rq_stats["queues"]
            for queue in queues:
                queue_name = queue["name"]
                django_rq_workers_count.add_metric([queue_name], queue["workers"])
        return django_rq_workers_count

    @staticmethod
    def get_django_rq_job_count():
        django_rq_job_count = GaugeMetricFamily(
            "django_rq_job_count",
            'Number of jobs',
            labels=['state', 'queue']
        )

        django_rq_stats = get_statistics()
        if "queues" in django_rq_stats:
            queues = django_rq_stats["queues"]
            for queue in queues:
                queue_name = queue["name"]
                django_rq_job_count.add_metric(["failed", queue_name], queue["failed_jobs"])
                django_rq_job_count.add_metric(["started", queue_name], queue["started_jobs"])
                django_rq_job_count.add_metric(["finished", queue_name], queue["finished_jobs"])
                django_rq_job_count.add_metric(["deferred", queue_name], queue["deferred_jobs"])
                django_rq_job_count.add_metric(["scheduled", queue_name], queue["scheduled_jobs"])
        return django_rq_job_count
