from rest_framework.test import APITestCase


class CommonModelTests(APITestCase):
    fixtures = ["data.json"]

    def test_共通カラムもレスポンスに含まれる(self):
        response = self.client.get("/common-model/")
        self.assertContains(response, "created_at")
        self.assertContains(response, "updated_at")

    def test_共通カラムの更新日時も自動で更新される(self):
        req_body = {"title": "posted data"}
        response = self.client.post("/common-model/", req_body)
        self.assertContains(response, "posted data", status_code=201)
        self.assertContains(response, "created_at", status_code=201)
        self.assertContains(response, "updated_at", status_code=201)
