"""Yesterday's wall, now with parcels in it."""

from tests.conftest import drop


def test_free_counts_the_filtered_doors(client):
    drop(client, "L", "302")
    assert client.get("/towers/A/doors").json()["free"] == 47
    large = client.get("/towers/A/doors?size=L").json()
    assert len(large["doors"]) == 8 and large["free"] == 7

    assert client.get("/towers/A/doors?size=S").json()["free"] == 20
    holding = client.get("/towers/A/doors?state=holding").json()
    assert len(holding["doors"]) == 1 and holding["free"] == 0


def test_holding_door_shows_parcel_and_dwell(client, clock):
    d = drop(client)
    clock.advance(hours=3, minutes=30)
    body = client.get("/towers/A/doors?state=holding").json()
    assert len(body["doors"]) == 1
    door = body["doors"][0]
    assert door == {
        "no": d["door"],
        "size": "M",
        "state": "holding",
        "parcel_id": d["parcel_id"],
        "dwell_seconds": 12600,
    }


def test_one_door(client, clock):
    d = drop(client, "S", "104")
    clock.advance(hours=3, minutes=30)
    body = client.get(f"/towers/A/doors/{d['door']}").json()
    assert body == {
        "no": d["door"],
        "size": "S",
        "state": "holding",
        "parcel_id": d["parcel_id"],
        "flat": "104",
        "dwell_seconds": 12600,
    }
    assert client.get("/towers/A/doors/D02").json() == {"no": "D02", "size": "S", "state": "free"}