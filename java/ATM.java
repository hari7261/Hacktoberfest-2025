import java.util.*;

public class ATM {

    static Scanner scan = new Scanner(System.in);
    static int balance_amount = 10000;
    static int withdraw_amount, deposit_amount;
    static int currentPin = 1234;

    // Method to validate ATM Card
    static boolean validate() {

        int i = 0;
        boolean res;
        do {

            //get pin from user
            System.out.print("Enter Pin: ");
            int givenPin = scan.nextInt();

            //check whether the pin is correct or not
            if (givenPin == currentPin) {
                
                res = true;
                break;

            } else {
                
                res = false;
                System.out.println("Wrong pin");
            
            }
            i++;
        
        } while (i < 3);
        
        
        if (i == 3) {
            System.out.println("Your card has been blocked\nPlease contact your bank");
            end();
        }

        return res;
    }

    // method to available balance
    static void balance() {

        if (validate()) {

            System.out.println("Available Balance: " + balance_amount);

        } else {

            System.out.println("Incorrect Pin ");
        }
    }

    // method to withdraw amount
    static void withdraw() {

        // get amount to be withdrawn from user
        System.out.print("Enter Withdrawn Amount: ");
        withdraw_amount = scan.nextInt();

        if (validate()) {

            // check whether balance is sufficient or not
            if (balance_amount >= withdraw_amount) {

                // Remaining Amount
                balance_amount -= withdraw_amount;

                System.out.println("Please collect your money");
                System.out.println("Available Balance: " + balance_amount);
                
            } else {

                // display error message
                System.out.println("Insufficient Balance...");
            }

        } else {
            System.out.println(" Incorrect Pin");
        }

    }

    // method to deposit amount
    static void deposit() {

        // Get deposit amount from user
        System.out.print("Enter the deposit Amount: ");
        deposit_amount = scan.nextInt();

        if (validate()) {

            // Total Amount
            balance_amount += deposit_amount;

            System.out.println("Your Money has been deposited successfully");
            System.out.println("Available Balance: " + balance_amount);

        } else {

            System.out.println(" Incorrect Pin ");
        }

    }

    // Method to Change Pin
    static void changePin() {

        if (validate()) {

            // get new pin from user
            System.out.print("Enter new pin: ");
            int newPin = scan.nextInt();

            // get confirm new pin from user
            System.out.print("Enter confirm new pin: ");
            int confirmNewPin = scan.nextInt();

            if (newPin == confirmNewPin) {

                currentPin = newPin;
                System.out.println("ATM Pin has been changed successfully");

            } else {

                System.out.println("New pin and Confirm new Pin does not match ");
            }

        }

    }

    static void end() {
        System.exit(0);
    }

    public static void main(String[] args) {

        // Scanner sc = new Scanner(System.in);
        // ATM atm = new ATM();

        while (true) {

            System.out.println("\nExcel ATM Service ");
            System.out.println("Choose 1 for Check Balance");
            System.out.println("Choose 2 for Withdraw");
            System.out.println("Choose 3 for Deposit");
            System.out.println("Choose 4 for Change Pin");
            System.out.println("Choose 5 for Exit\n");

            // get operation from user
            System.out.print("Enter Operation: ");
            int operation = scan.nextInt();

            switch (operation) {

                case 1:
                    balance();
                    break;

                case 2:
                    withdraw();
                    break;

                case 3:
                    deposit();
                    break;

                case 4:
                    changePin();
                    break;

                case 5:
                    System.out.println("Thank You ");
                    end();

                default:
                    System.out.println("Invalid Input");

            }

        }
    }
}
