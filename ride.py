class RideBooking:

    def __init__(self):

        self.vehicles = {
            "Bike": {
                "base": 30,
                "per_km": 10,
                "max_passengers": 1
            },

            "Sedan": {
                "base": 60,
                "per_km": 15,
                "max_passengers": 4
            },

            "SUV": {
                "base": 80,
                "per_km": 20,
                "max_passengers": 6
            },

            "Premium": {
                "base": 120,
                "per_km": 30,
                "max_passengers": 4
            }
        }

        self.drivers = {
            "D001": {
                "vehicle": "Bike",
                "available": True
            },

            "D002": {
                "vehicle": "Sedan",
                "available": True
            },

            "D003": {
                "vehicle": "SUV",
                "available": True
            },

            "D004": {
                "vehicle": "Premium",
                "available": True
            }
        }

    # ----------------------------------------
    # Validate Booking
    # ----------------------------------------
    def validate_booking(
        self,
        distance,
        passengers,
        vehicle_type,
        booking_time
    ):

        if distance <= 0:
            return False

        if passengers <= 0:
            return False

        if vehicle_type not in self.vehicles:
            return False

        max_passengers = self.vehicles[
            vehicle_type
        ]["max_passengers"]

        if passengers > max_passengers:
            return False

        if booking_time < 0 or booking_time > 23:
            return False

        return True

    # ----------------------------------------
    # Peak Hour
    # ----------------------------------------
    def peak_hour(self, booking_time):

        if 7 <= booking_time <= 10:
            return True

        if 17 <= booking_time <= 20:
            return True

        return False

    # ----------------------------------------
    # Night Hour
    # ----------------------------------------
    def night_hour(self, booking_time):

        if booking_time >= 22 or booking_time < 6:
            return True

        return False

    # ----------------------------------------
    # Calculate Fare
    # ----------------------------------------
    def calculate_fare(
        self,
        distance,
        passengers,
        vehicle_type,
        booking_time,
        promotional_discount
    ):

        valid = self.validate_booking(
            distance,
            passengers,
            vehicle_type,
            booking_time
        )

        if not valid:
            return None

        vehicle = self.vehicles[vehicle_type]

        # Base fare
        base_fare = vehicle["base"]

        # Distance fare
        distance_fare = (
            distance * vehicle["per_km"]
        )

        # Peak surcharge
        peak_surcharge = 0

        if self.peak_hour(booking_time):
            peak_surcharge = base_fare * 0.25

        # Night surcharge
        night_surcharge = 0

        if self.night_hour(booking_time):
            night_surcharge = base_fare * 0.20

        # Passenger surcharge
        passenger_surcharge = 0

        if passengers > 1:
            passenger_surcharge = (
                passengers - 1
            ) * 20

        # Subtotal
        subtotal = (
            base_fare
            + distance_fare
            + peak_surcharge
            + night_surcharge
            + passenger_surcharge
        )

        # Promotional discount
        if promotional_discount < 0:
            promotional_discount = 0

        if promotional_discount > subtotal:
            promotional_discount = subtotal

        # Final fare
        final_fare = (
            subtotal - promotional_discount
        )

        return {
            "base_fare": base_fare,
            "distance_fare": distance_fare,
            "peak_surcharge": peak_surcharge,
            "night_surcharge": night_surcharge,
            "passenger_surcharge": passenger_surcharge,
            "promotional_discount": promotional_discount,
            "final_fare": final_fare
        }

    # ----------------------------------------
    # Driver Assignment
    # ----------------------------------------
    def assign_driver(self, vehicle_type):

        for driver_id in self.drivers:

            driver = self.drivers[driver_id]

            if (
                driver["vehicle"] == vehicle_type
                and driver["available"] is True
            ):

                driver["available"] = False

                return driver_id

        return None

    # ----------------------------------------
    # Create Booking
    # ----------------------------------------
    def create_booking(
        self,
        customer_id,
        pickup,
        drop,
        distance,
        passengers,
        vehicle_type,
        booking_time,
        promotional_discount=0
    ):

        if customer_id == "":
            return None

        if pickup == "":
            return None

        if drop == "":
            return None

        fare = self.calculate_fare(
            distance,
            passengers,
            vehicle_type,
            booking_time,
            promotional_discount
        )

        if fare is None:
            return None

        driver_id = self.assign_driver(
            vehicle_type
        )

        if driver_id is None:
            return None

        booking = {
            "customer_id": customer_id,
            "pickup": pickup,
            "drop": drop,
            "distance": distance,
            "passengers": passengers,
            "vehicle_type": vehicle_type,
            "booking_time": booking_time,
            "driver_id": driver_id,
            "fare": fare
        }

        return booking


# ============================================
# MAIN PROGRAM
# ============================================

if __name__ == "__main__":

    ride = RideBooking()

    booking = ride.create_booking(
        "C001",
        "Chennai",
        "Tambaram",
        10,
        2,
        "Sedan",
        14,
        20
    )

    print("================================")
    print("      RIDE BOOKING SYSTEM")
    print("================================")

    if booking is not None:

        print("Booking Successful")
        print()
        print("Customer ID :", booking["customer_id"])
        print("Pickup      :", booking["pickup"])
        print("Drop        :", booking["drop"])
        print("Distance    :", booking["distance"])
        print("Passengers  :", booking["passengers"])
        print("Vehicle     :", booking["vehicle_type"])
        print("Driver      :", booking["driver_id"])

        print()
        print("Base Fare           :",
              booking["fare"]["base_fare"])

        print("Distance Fare       :",
              booking["fare"]["distance_fare"])

        print("Peak Surcharge      :",
              booking["fare"]["peak_surcharge"])

        print("Night Surcharge     :",
              booking["fare"]["night_surcharge"])

        print("Passenger Surcharge :",
              booking["fare"]["passenger_surcharge"])

        print("Discount            :",
              booking["fare"]["promotional_discount"])

        print("Final Fare          :",
              booking["fare"]["final_fare"])

    else:

        print("Booking Rejected")
