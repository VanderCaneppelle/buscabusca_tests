
def test_get_webhook(session, base_url):
    response = session.get(base_url)
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == 'Webhook test endpoint is working!'
    assert "timestamp" in data


def test_post_not_payment(session, base_url, not_payment_payload):

    response = session.post(base_url, json=not_payment_payload)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"].startswith("Webhook ignored")


def test_post_payment(session, base_url, payment_correct_payload):

    response = session.post(base_url, json=payment_correct_payload)

    # Pode variar entre 404 (não encontrou pagamento) ou 500 (erro interno)
    assert response.status_code in [500, 404]
    data = response.json()
    assert "error" in data or "message" in data
    assert data["message"] == "Erro ao buscar pagamento: 404"


def test_put_method(session, base_url):
    response = session.put(base_url)

    assert response.status_code == 405
    data = response.json()
    assert data["error"] == "Method not allowed"
