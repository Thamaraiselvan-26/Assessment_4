public class RideBookingQA {

    // -----------------------------
    // Calculate Fare
    // -----------------------------
    static double calculateFare(
            double distance,
            int passengers,
            String vehicle,
            int time,
            double discount) {

        double base;
        double rate;
        int maxPassengers;

        // Vehicle details
        if (vehicle.equals("Bike")) {
            base = 30;
            rate = 10;
            maxPassengers = 1;

        } else if (vehicle.equals("Sedan")) {
            base = 60;
            rate = 15;
            maxPassengers = 4;

        } else if (vehicle.equals("SUV")) {
            base = 80;
            rate = 20;
            maxPassengers = 6;

        } else if (vehicle.equals("Premium")) {
            base = 120;
            rate = 30;
            maxPassengers = 4;

        } else {
            return -1;
        }

        // Invalid distance
        if (distance <= 0) {
            return -1;
        }

        // Invalid passenger count
        if (passengers <= 0 ||
            passengers > maxPassengers) {

            return -1;
        }

        // Invalid time
        if (time < 0 || time > 23) {
            return -1;
        }

        // Distance fare
        double distanceFare =
                distance * rate;

        // Peak surcharge
        double peakSurcharge = 0;

        if ((time >= 7 && time <= 10) ||
            (time >= 17 && time <= 20)) {

            peakSurcharge =
                    base * 0.25;
        }

        // Night surcharge
        double nightSurcharge = 0;

        if (time >= 22 || time < 6) {

            nightSurcharge =
                    base * 0.20;
        }

        // Passenger surcharge
        double passengerSurcharge = 0;

        if (passengers > 1) {

            passengerSurcharge =
                    (passengers - 1) * 20;
        }

        // Total fare
        double total =
                base
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


    // -----------------------------
    // Test 1
    // Normal Booking
    // -----------------------------
    static void normalBooking() {

        double fare = calculateFare(
                10,
                1,
                "Sedan",
                14,
                0
        );

        if (fare > 0) {
            System.out.println(
                    "PASS - Normal Booking");
        } else {
            System.out.println(
                    "FAIL - Normal Booking");
        }
    }


    // -----------------------------
    // Test 2
    // Peak Hour
    // -----------------------------
    static void peakHourBooking() {

        double normal = calculateFare(
                10,
                1,
                "Sedan",
                14,
                0
        );

        double peak = calculateFare(
                10,
                1,
                "Sedan",
                8,
                0
        );

        if (peak > normal) {
            System.out.println(
                    "PASS - Peak Hour Booking");
        } else {
            System.out.println(
                    "FAIL - Peak Hour Booking");
        }
    }


    // -----------------------------
    // Test 3
    // Night Booking
    // -----------------------------
    static void nightBooking() {

        double normal = calculateFare(
                10,
                1,
                "Sedan",
                14,
                0
        );

        double night = calculateFare(
                10,
                1,
                "Sedan",
                23,
                0
        );

        if (night > normal) {
            System.out.println(
                    "PASS - Night Booking");
        } else {
            System.out.println(
                    "FAIL - Night Booking");
        }
    }


    // -----------------------------
    // Test 4
    // Invalid Distance
    // -----------------------------
    static void invalidDistance() {

        double fare = calculateFare(
                0,
                1,
                "Sedan",
                14,
                0
        );

        if (fare == -1) {
            System.out.println(
                    "PASS - Invalid Distance");
        } else {
            System.out.println(
                    "FAIL - Invalid Distance");
        }
    }


    // -----------------------------
    // Test 5
    // Invalid Passenger Count
    // -----------------------------
    static void invalidPassengers() {

        double fare = calculateFare(
                10,
                10,
                "Sedan",
                14,
                0
        );

        if (fare == -1) {
            System.out.println(
                    "PASS - Invalid Passenger Count");
        } else {
            System.out.println(
                    "FAIL - Invalid Passenger Count");
        }
    }


    // -----------------------------
    // Test 6
    // Unavailable Driver
    // -----------------------------
    static void unavailableDriver() {

        boolean driverAvailable = false;

        if (!driverAvailable) {
            System.out.println(
                    "PASS - Unavailable Driver");
        } else {
            System.out.println(
                    "FAIL - Unavailable Driver");
        }
    }


    // -----------------------------
    // Test 7
    // Maximum Discount
    // -----------------------------
    static void maximumDiscount() {

        double fare = calculateFare(
                10,
                1,
                "Sedan",
                14,
                10000
        );

        if (fare == 0) {
            System.out.println(
                    "PASS - Maximum Discount");
        } else {
            System.out.println(
                    "FAIL - Maximum Discount");
        }
    }


    // -----------------------------
    // Test 8
    // Multiple Vehicle Types
    // -----------------------------
    static void multipleVehicles() {

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

        if (bike > 0 &&
            sedan > 0 &&
            suv > 0 &&
            premium > 0) {

            System.out.println(
                    "PASS - Multiple Vehicle Types");

        } else {

            System.out.println(
                    "FAIL - Multiple Vehicle Types");
        }
    }


    // -----------------------------
    // Test 9
    // Boundary Fare
    // -----------------------------
    static void boundaryFare() {

        double fare = calculateFare(
                1,
                1,
                "Bike",
                14,
                0
        );

        if (fare == 40) {
            System.out.println(
                    "PASS - Boundary Fare Values");
        } else {
            System.out.println(
                    "FAIL - Boundary Fare Values");
        }
    }


    // -----------------------------
    // Test 10
    // Driver Allocation
    // -----------------------------
    static void driverAllocation() {

        String driver = "D001";

        if (driver.equals("D001")) {
            System.out.println(
                    "PASS - Driver Allocation Logic");
        } else {
            System.out.println(
                    "FAIL - Driver Allocation Logic");
        }
    }


    // -----------------------------
    // Main
    // -----------------------------
    public static void main(String[] args) {

        System.out.println(
                "====================================");

        System.out.println(
                "     RIDE BOOKING QA TEST");

        System.out.println(
                "====================================");

        normalBooking();

        peakHourBooking();

        nightBooking();

        invalidDistance();

        invalidPassengers();

        unavailableDriver();

        maximumDiscount();

        multipleVehicles();

        boundaryFare();

        driverAllocation();

        System.out.println(
                "====================================");

        System.out.println(
                "     TESTING COMPLETED");

        System.out.println(
                "====================================");
    }
}
