import csv
from django.db.models import QuerySet
from django.db.models.options import Options
from django.http import HttpRequest, HttpResponse
from django.core import serializers


class ExportMixin:
    def export_as_json(self, request: HttpRequest, queryset: QuerySet):
        meta: Options = self.model._meta
        data = serializers.serialize("json", queryset)
        response = HttpResponse(data, content_type="application/json")
        response["Content-Disposition"] = f"attachment; filename={meta}-export.json"

        return response

    export_as_json.short_description = "Export as JSON"

    def export_as_csv(self, request: HttpRequest, queryset: QuerySet):
        meta: Options = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}-export.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export as CSV"
