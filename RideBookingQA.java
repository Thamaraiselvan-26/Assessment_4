public class RideBookingQA {

    // ==========================================
    // Vehicle Class
    // ==========================================

    static class Vehicle {

        String type;
        double baseFare;
        double perKm;
        int maxPassengers;

        Vehicle(
                String type,
                double baseFare,
                double perKm,
                int maxPassengers) {

            this.type = type;
            this.baseFare = baseFare;
            this.perKm = perKm;
            this.maxPassengers = maxPassengers;
        }
    }

    // ==========================================
    // Driver Class
    // ==========================================

    static class Driver {

        String driverId;
        String vehicleType;
        boolean available;

        Driver(
                String driverId,
                String vehicleType,
                boolean available) {

            this.driverId = driverId;
            this.vehicleType = vehicleType;
            this.available = available;
        }
    }

    // ==========================================
    // Fare Calculation
    // ==========================================

    static double calculateFare(
            double distance,
            int passengers,
            String vehicleType,
            int bookingTime,
            double discount) {

        double baseFare;
        double perKm;
        int maxPassengers;

        if (vehicleType.equals("Bike")) {

            baseFare = 30;
            perKm = 10;
            maxPassengers = 1;

        } else if (vehicleType.equals("Sedan")) {

            baseFare = 60;
            perKm = 15;
            maxPassengers = 4;

        } else if (vehicleType.equals("SUV")) {

            baseFare = 80;
            perKm = 20;
            maxPassengers = 6;

        } else if (vehicleType.equals("Premium")) {

            baseFare = 120;
            perKm = 30;
            maxPassengers = 4;

        } else {

            return -1;
        }

        // Invalid distance
        if (distance <= 0) {
            return -1;
        }

        // Invalid passengers
        if (passengers <= 0) {
            return -1;
        }

        if (passengers > maxPassengers) {
            return -1;
        }

        // Invalid booking time
        if (bookingTime < 0 || bookingTime > 23) {
            return -1;
        }

        // Distance fare
        double distanceFare =
                distance * perKm;

        // Peak surcharge
        double peakSurcharge = 0;

        if ((bookingTime >= 7 && bookingTime <= 10)
                || (bookingTime >= 17
                && bookingTime <= 20)) {

            peakSurcharge = baseFare * 0.25;
        }

        // Night surcharge
        double nightSurcharge = 0;

        if (bookingTime >= 22
                || bookingTime < 6) {

            nightSurcharge = baseFare * 0.20;
        }

        // Passenger surcharge
        double passengerSurcharge = 0;

        if (passengers > 1) {

            passengerSurcharge =
                    (passengers - 1) * 20;
        }

        // Total before discount
        double total =
                baseFare
                + distanceFare
                + peakSurcharge
                + nightSurcharge
                + passengerSurcharge;

        // Discount
        if (discount < 0) {
            discount = 0;
        }

        if (discount > total) {
            discount = total;
        }

        return total - discount;
    }

    // ==========================================
    // Driver Assignment
    // ==========================================

    static String assignDriver(
            Driver[] drivers,
            String vehicleType) {

        for (Driver driver : drivers) {

            if (driver.vehicleType.equals(vehicleType)
                    && driver.available) {

                driver.available = false;

                return driver.driverId;
            }
        }

        return null;
    }

    // ==========================================
    // Test Counter
    // ==========================================

    static int passed = 0;
    static int failed = 0;

    static void checkTest(
            String testName,
            boolean result) {

        if (result) {

            System.out.println(
                    "PASS - " + testName);

            passed++;

        } else {

            System.out.println(
                    "FAIL - " + testName);

            failed++;
        }
    }

    // ==========================================
    // 1. Normal Booking
    // ==========================================

    static void testNormalBooking() {

        double fare = calculateFare(
                10,
                2,
                "Sedan",
                14,
                0
        );

        checkTest(
                "Normal Booking",
                fare > 0
        );
    }

    // ==========================================
    // 2. Peak Hour Booking
    // ==========================================

    static void testPeakHourBooking() {

        double normalFare = calculateFare(
                10,
                1,
                "Sedan",
                14,
                0
        );

        double peakFare = calculateFare(
                10,
                1,
                "Sedan",
                8,
                0
        );

        checkTest(
                "Peak-hour Booking",
                peakFare > normalFare
        );
    }

    // ==========================================
    // 3. Night Booking
    // ==========================================

    static void testNightBooking() {

        double normalFare = calculateFare(
                10,
                1,
                "Sedan",
                14,
                0
        );

        double nightFare = calculateFare(
                10,
                1,
                "Sedan",
                23,
                0
        );

        checkTest(
                "Night Booking",
                nightFare > normalFare
        );
    }

    // ==========================================
    // 4. Invalid Distance
    // ==========================================

    static void testInvalidDistance() {

        double fare = calculateFare(
                0,
                1,
                "Sedan",
                14,
                0
        );

        checkTest(
                "Invalid Distance",
                fare == -1
        );
    }

    // ==========================================
    // 5. Invalid Passenger Count
    // ==========================================

    static void testInvalidPassengerCount() {

        double fare = calculateFare(
                10,
                10,
                "Sedan",
                14,
                0
        );

        checkTest(
                "Invalid Passenger Count",
                fare == -1
        );
    }

    // ==========================================
    // 6. Unavailable Driver
    // ==========================================

    static void testUnavailableDriver() {

        Driver[] drivers = {

            new Driver(
                    "D001",
                    "Sedan",
                    false
            ),

            new Driver(
                    "D002",
                    "SUV",
                    true
            )
        };

        String driver =
                assignDriver(
                        drivers,
                        "Sedan"
                );

        checkTest(
                "Unavailable Driver",
                driver == null
        );
    }

    // ==========================================
    // 7. Maximum Discount
    // ==========================================

    static void testMaximumDiscount() {

        double fare = calculateFare(
                10,
                1,
                "Sedan",
                14,
                10000
        );

        checkTest(
                "Maximum Discount",
                fare == 0
        );
    }

    // ==========================================
    // 8. Multiple Vehicle Types
    // ==========================================

    static void testMultipleVehicleTypes() {

        double bike = calculateFare(
                10,
                1,
                "Bike",
                14,
                0
        );

        double sedan = calculateFare(
                10,
                2,
                "Sedan",
                14,
                0
        );

        double suv = calculateFare(
                10,
                4,
                "SUV",
                14,
                0
        );

        double premium = calculateFare(
                10,
                2,
                "Premium",
                14,
                0
        );

        checkTest(
                "Multiple Vehicle Types",
                bike > 0
                && sedan > 0
                && suv > 0
                && premium > 0
        );
    }

    // ==========================================
    // 9. Boundary Fare Values
    // ==========================================

    static void testBoundaryFareValues() {

        double fare = calculateFare(
                1,
                1,
                "Bike",
                14,
                0
        );

        checkTest(
                "Boundary Fare Values",
                fare == 40
        );
    }

    // ==========================================
    // 10. Driver Allocation Logic
    // ==========================================

    static void testDriverAllocation() {

        Driver[] drivers = {

            new Driver(
                    "D001",
                    "Bike",
                    true
            ),

            new Driver(
                    "D002",
                    "Sedan",
                    true
            )
        };

        String driver =
                assignDriver(
                        drivers,
                        "Bike"
                );

        checkTest(
                "Driver Allocation Logic",
                driver != null
                && driver.equals("D001")
                && !drivers[0].available
        );
    }

    // ==========================================
    // MAIN
    // ==========================================

    public static void main(String[] args) {

        System.out.println();
        System.out.println(
                "========================================"
        );

        System.out.println(
                "       RIDE BOOKING QA TEST"
        );

        System.out.println(
                "========================================"
        );

        testNormalBooking();

        testPeakHourBooking();

        testNightBooking();

        testInvalidDistance();

        testInvalidPassengerCount();

        testUnavailableDriver();

        testMaximumDiscount();

        testMultipleVehicleTypes();

        testBoundaryFareValues();

        testDriverAllocation();

        System.out.println();

        System.out.println(
                "========================================"
        );

        System.out.println(
                "Tests Passed : " + passed
        );

        System.out.println(
                "Tests Failed : " + failed
        );

        System.out.println(
                "========================================"
        );

        if (failed == 0) {

            System.out.println(
                    "ALL TESTS PASSED"
            );

            System.exit(0);

        } else {

            System.out.println(
                    "TESTS FAILED"
            );

            System.exit(1);
        }
    }
}
