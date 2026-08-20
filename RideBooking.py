from datetime import datetime


class RideBooking:

    def __init__(self):

        self.base_fare = {
            "Bike": 30,
            "Sedan": 60,
            "SUV": 100,
            "Premium": 150
        }

        self.per_km = {
            "Bike": 10,
            "Sedan": 15,
            "SUV": 20,
            "Premium": 30
        }

        self.capacity = {
            "Bike": 1,
            "Sedan": 4,
            "SUV": 6,
            "Premium": 4
        }

        self.drivers = {
            "Bike": ["B101", "B102"],
            "Sedan": ["S101", "S102"],
            "SUV": ["U101"],
            "Premium": ["P101"]
        }

    def book_ride(self, customer_id, pickup, drop,
                  distance, passengers, vehicle, booking_time):

        if distance <= 0:
            return False, "Invalid distance"

        if passengers <= 0:
            return False, "Invalid passenger count"

        if vehicle not in self.capacity:
            return False, "Unavailable vehicle"

        if passengers > self.capacity[vehicle]:
            return False, "Excessive passengers"

        try:
            time = datetime.strptime(booking_time, "%H:%M")
        except ValueError:
            return False, "Invalid booking time"

        if len(self.drivers[vehicle]) == 0:
            return False, "Driver unavailable"

        base = self.base_fare[vehicle]
        distance_fare = distance * self.per_km[vehicle]

        if (7 <= time.hour < 10) or (17 <= time.hour < 21):
            peak = (base + distance_fare) * 0.25
        else:
            peak = 0

        if time.hour >= 22 or time.hour < 6:
            night = (base + distance_fare) * 0.20
        else:
            night = 0

        passenger_charge = (passengers - 1) * 20

        if distance >= 20:
            discount = (base + distance_fare) * 0.10
        else:
            discount = 0

        final_fare = (
            base
            + distance_fare
            + peak
            + night
            + passenger_charge
            - discount
        )

        driver = self.drivers[vehicle][0]

        return True, {
            "Customer": customer_id,
            "Pickup": pickup,
            "Drop": drop,
            "Vehicle": vehicle,
            "Base Fare": round(base, 2),
            "Distance Fare": round(distance_fare, 2),
            "Peak Surcharge": round(peak, 2),
            "Night Surcharge": round(night, 2),
            "Passenger Surcharge": round(passenger_charge, 2),
            "Discount": round(discount, 2),
            "Final Fare": round(final_fare, 2),
            "Driver": driver
        }


# Predefined booking
if __name__ == "__main__":

    ride = RideBooking()

    success, result = ride.book_ride(
        "C101",
        "Vellore",
        "Chennai",
        25,
        2,
        "Sedan",
        "18:30"
    )

    if success:
        print("BOOKING SUCCESSFUL")

        for key, value in result.items():
            print(key + ":", value)

    else:
        print("BOOKING FAILED")
        print(result)