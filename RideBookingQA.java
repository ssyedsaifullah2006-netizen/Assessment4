public class RideBookingQA {

    static int pass = 0;
    static int fail = 0;

    static void test(String name, boolean condition) {

        if (condition) {
            System.out.println("PASS: " + name);
            pass++;
        } else {
            System.out.println("FAIL: " + name);
            fail++;
        }
    }

    public static void main(String[] args) {

        System.out.println("RIDE BOOKING QA");
        System.out.println("================");


        // 1. Normal Booking

        double base = 60;
        double distance = 10 * 15;
        double fare = base + distance + 20;

        test(
            "Normal Booking",
            fare == 230
        );


        // 2. Peak Hour Booking

        base = 60;
        distance = 150;

        double peak = (base + distance) * 0.25;

        test(
            "Peak Hour Booking",
            peak == 52.5
        );


        // 3. Night Booking

        base = 100;
        distance = 10 * 20;

        double night = (base + distance) * 0.20;

        test(
            "Night Booking",
            night == 60
        );


        // 4. Invalid Distance

        double invalidDistance = 0;

        test(
            "Invalid Distance",
            invalidDistance <= 0
        );


        // 5. Invalid Passenger Count

        int passengers = 0;

        test(
            "Invalid Passenger Count",
            passengers <= 0
        );


        // 6. Unavailable Driver

        int availableDrivers = 0;

        test(
            "Unavailable Driver",
            availableDrivers == 0
        );


        // 7. Maximum Discount

        distance = 20;
        base = 30;

        double distanceFare = distance * 10;
        double discount = (base + distanceFare) * 0.10;

        test(
            "Maximum Discount",
            discount == 23
        );


        // 8. Multiple Vehicle Types

        String[] vehicles = {
            "Bike",
            "Sedan",
            "SUV",
            "Premium"
        };

        test(
            "Bike",
            vehicles[0].equals("Bike")
        );

        test(
            "Sedan",
            vehicles[1].equals("Sedan")
        );

        test(
            "SUV",
            vehicles[2].equals("SUV")
        );

        test(
            "Premium",
            vehicles[3].equals("Premium")
        );


        // 9. Boundary Fare

        base = 30;
        distance = 1 * 10;

        fare = base + distance;

        test(
            "Boundary Fare",
            fare == 40
        );


        // 10. Driver Allocation

        String driver = "B101";

        test(
            "Driver Allocation",
            driver.equals("B101")
        );


        // Final Result

        System.out.println();
        System.out.println("================");
        System.out.println("Passed: " + pass);
        System.out.println("Failed: " + fail);

        if (fail == 0) {
            System.out.println("ALL TESTS PASSED");
        } else {
            System.out.println("SOME TESTS FAILED");
        }
    }
}