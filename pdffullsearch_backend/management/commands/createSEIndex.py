import time
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from elasticsearch_dsl.connections import connections
from pdffullsearch_backend.documents import PDFFileDocument


class Command(BaseCommand):
    help = 'Create index defined on documents.py'

    def handle(self, *args, **options):
        try:
            tries = 0
            while(tries < 5):
                try:
                    es = connections.get_connection()
                    es.ping()
                    break
                except Exception as e:
                    tries += 1
                    self.stdout.write(self.style.WARNING(f"Attempt {tries}: Could not connect to Elasticsearch, retrying..."))
                    time.sleep(5)  # Wait for 5 seconds before retrying

            es = connections.get_connection()                
            # Check if the index exists and create if not
            index_name = PDFFileDocument._index._name
            if not es.indices.exists(index=index_name):
                self.stdout.write(f"Elasticsearch index '{index_name}' not found, creating...")
                # The Document class has a method to create its index
                PDFFileDocument.init() 
                self.stdout.write(f"Elasticsearch index '{index_name}' created.")
            else:
                self.stdout.write(f"Elasticsearch index '{index_name}' already exists.")
        except ConnectionError:
            self.stdout.write(self.style.ERROR("Could not connect to Elasticsearch, skipping index creation."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred during index creation: {e}"))
