from PyQt6.QtWidgets import *
from lab9_gui import *
import pickle
import atexit


class Logic(QMainWindow, Ui_MainWindow):
    __profiles = {'JohnDoe2121': {'checking': {'personal': 2000.00, 'house': 2000.00}, 'saving': {'vacation': 200.00,
                                                                                                  'car': 323.02}}}

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__login_profile = ''
        self.current_account = 0
        self.__profile_info = []
        self.profile_load()
        print(Logic.__profiles)

        self.new_account_button.clicked.connect(lambda: self.new_acc_btn())
        self.new_profile_button.clicked.connect(lambda: self.new_acc_btn())
        self.logout_button.clicked.connect(lambda: self.logout_btn())
        self.home_button.clicked.connect(lambda: self.logout_btn())

        self.login_button.clicked.connect(lambda: self.login())
        self.confirm_button.clicked.connect(lambda: self.confirm())
        self.new_pro_checkbox.clicked.connect(lambda: self.new_pro_check())
        self.acc_button.clicked.connect(lambda: self.acc_btn())
        self.next_button.clicked.connect(lambda: self.next_btn())
        self.previous_button.clicked.connect(lambda: self.prev_btn())
        self.submit_button.clicked.connect(lambda: self.submit())
        atexit.register(self.exit_handler)

    def exit_handler(self):
        self.profiles_save()

    def profiles_save(self):
        with open('profiles.pickle', 'wb') as file:
            pickle.dump(Logic.__profiles, file)

    def profile_load(self):
        try:
            with open('profiles.pickle', 'rb') as file:
                Logic.__profiles = pickle.load(file)
                print(pickle.load(file))
        except:
            pass

    def ui_update(self) -> None:
        """
        Function to clear text and set placeholder text to default values
        :return:
        """
        self.first_name_input.clear()
        self.pro_f_name_input.clear()
        self.pro_f_name_input.setPlaceholderText('Enter First Name for Profile')
        self.last_name_input.clear()
        self.pro_l_name_input.clear()
        self.pro_l_name_input.setPlaceholderText('Enter Last Name for Profile')
        self.password_input.clear()
        self.pro_pass_input.clear()
        self.pro_pass_input.setPlaceholderText('Enter Password for Profile')
        self.amount_input_accounts.clear()
        self.new_name_input.clear()
        self.new_name_input.setPlaceholderText('Enter Account Name')
        self.new_deposit_input.clear()
        self.new_deposit_input.setPlaceholderText('Enter Deposit Amount')
        self.amount_input_accounts.clear()
        self.amount_input_accounts.setPlaceholderText('Enter Total Amount')
        self.deposit_radio.setChecked(True)
        if self.__login_profile != '':
            self.acc_button.setEnabled(True)
        else:
            self.acc_button.setEnabled(False)

    def new_acc_btn(self) -> None:
        """
        Switches the stacked widget to the new accounts page and clears inputs
        :return:
        """
        self.stackedWidget.setCurrentIndex(2)
        self.ui_update()

    def current_profile_accs(self) -> None:
        """
        Converts the information about the account wanting to be accessed to allow for easier manipulation
        and stores it in the current_account list
        :return:
        """
        self.__profile_info.clear()
        for acc_type in Logic.__profiles[self.__login_profile]:
            for acc_name, acc_bal in Logic.__profiles[self.__login_profile][acc_type].items():
                self.__profile_info.append([acc_type, acc_name, acc_bal])
        self.current_account = 0

    def set_account_info(self) -> None:
        """
        Sets the labels in the account page to display the information about the account being accessed
        :return:
        """
        account = self.__profile_info[self.current_account]
        self.account_type_label.setText(f'Type: {account[0]}')
        self.account_name.setText(f'Name: {account[1]}')
        self.balance_label.setText(f'Balance: ${account[2]: .2f}')

    def next_btn(self) -> None:
        """
        Sets the account info of the next account in the profile info list
        :return:
        """
        self.current_account += 1
        if self.current_account > len(self.__profile_info) - 1:
            self.current_account = 0
            self.set_account_info()
        else:
            self.set_account_info()

    def prev_btn(self) -> None:
        """
        Sets the account info of the previous account in the profile info list
        :return:
        """
        self.current_account -= 1
        if self.current_account < 0:
            self.current_account = len(self.__profile_info) - 1
            self.set_account_info()
        else:
            self.set_account_info()

    def logout_btn(self) -> None:
        """
        Switches the stacked widget to the home page and clears inputs while also resetting the profile being used
        to empty
        :return:
        """
        self.stackedWidget.setCurrentIndex(0)
        self.ui_update()
        self.current_account = 0
        self.__profile_info.clear()
        self.__login_profile = ''

    def acc_btn(self) -> None:
        """
        Switches the stacked widget to the accounts page and clears inputs
        :return:
        """
        self.stackedWidget.setCurrentIndex(1)
        self.ui_update()
        self.current_profile_accs()
        self.set_account_info()

    def login(self) -> None:
        """
        Checks if the information inputted is in the dictionary to allow the user to proceed to the accounts
        page and sets the profile being used
        :return:
        """
        f_name = self.first_name_input.text()
        l_name = self.last_name_input.text()
        password = self.password_input.text()
        login_info = f_name + l_name + password
        for key in Logic.__profiles:
            if login_info == key:
                self.__login_profile = login_info
                self.acc_btn()

    def new_account(self) -> None:
        """
        Creates a new account for the profile in use. It also checks if the account trying to be created already exist
        if so, then it doesn't create the account and tells the user to input to try a different name. Function also
        prevents non-numerical values from being entered for starting balance. Clears all input fields.
        :return:
        """
        acc_name = self.new_name_input.text().strip()
        start_balance = self.new_deposit_input.text().strip()
        try:
            if acc_name == '':
                raise NameError()
            for profile in Logic.__profiles:
                for acc_type in Logic.__profiles[profile]:
                    for account_name in Logic.__profiles[profile][acc_type]:
                        if account_name == acc_name:
                            raise KeyError
            if start_balance == '':
                raise TypeError
            start_balance = eval(start_balance)
            start_balance = float(start_balance)
            if self.checking_radio.isChecked():
                Logic.__profiles[self.__login_profile]['checking'][acc_name] = start_balance
            elif self.saving_radio.isChecked():
                Logic.__profiles[self.__login_profile]['saving'][acc_name] = start_balance
            self.ui_update()
        except TypeError:
            self.__login_profile = ''
            self.ui_update()
            self.new_deposit_input.setPlaceholderText('Enter a number amount (no characters ex: $#@~!)')
        except NameError:
            self.__login_profile = ''
            self.ui_update()
            self.new_name_input.setPlaceholderText('Enter a Name for the account')
        except KeyError:
            self.__login_profile = ''
            self.ui_update()
            self.new_name_input.setPlaceholderText('Account already Exists')
    def new_pro_check(self) -> None:
        """
        Enables and Disables profile creation depending on the checkbox state
        :return:
        """
        if self.new_pro_checkbox.isChecked():
            self.pro_f_name_label.setEnabled(True)
            self.pro_f_name_input.setEnabled(True)
            self.pro_l_name_label.setEnabled(True)
            self.pro_l_name_input.setEnabled(True)
            self.pro_pass_label.setEnabled(True)
            self.pro_pass_input.setEnabled(True)
        else:
            self.pro_f_name_label.setEnabled(False)
            self.pro_f_name_input.setEnabled(False)
            self.pro_l_name_label.setEnabled(False)
            self.pro_l_name_input.setEnabled(False)
            self.pro_pass_label.setEnabled(False)
            self.pro_pass_input.setEnabled(False)
        self.ui_update()

    def new_profile(self) -> None:
        """
        Creates a new profile and stores the created account alongside it. Checks for improper inputs and prevents
        already existing account from being overwritten
        :return:
        """
        f_name = self.pro_f_name_input.text().strip()
        l_name = self.pro_l_name_input.text().strip()
        password = self.pro_pass_input.text().strip()
        profile = f_name + l_name + password
        self.__profile_info.clear()
        self.new_pro_checkbox.setChecked(False)
        try:
            for existing_profile in Logic.__profiles:
                if existing_profile == profile:
                    raise KeyError
            if f_name == '' or l_name == '':
                raise TypeError
            elif len(password) < 3:
                raise NameError
            Logic.__profiles[profile] = {'checking': {}, 'saving': {}}
            self.__login_profile = profile
            print('before new account func')
            self.new_account()
            print(self.__login_profile)
            if self.__login_profile == '':
                Logic.__profiles.pop(profile)
            print(Logic.__profiles)
        except TypeError:
            self.pro_f_name_input.setPlaceholderText('Enter First Name')
            self.pro_l_name_input.setPlaceholderText('Enter Last Name')
        except NameError:
            self.pro_pass_input.setPlaceholderText('Enter a password at is 4 characters long minimum')
        except KeyError:
            self.pro_f_name_input.setPlaceholderText('Account already exists')
            self.pro_l_name_input.setPlaceholderText('Account already exists')
            self.pro_pass_input.setPlaceholderText('Account already exists')
            self.ui_update()
        finally:
            self.new_pro_check()

    def confirm(self) -> None:
        """
        Creates a new profile or account depending on whether the 'new profile' checkbox is checked or not
        :return:
        """
        if self.new_pro_checkbox.isChecked():
            self.new_profile()
        else:
            self.new_account()

    def submit(self) -> None:
        """
        Checks if whether the user is trying to deposit or withdraw a certain amount of money. Any invalid inputs of
        money are handled i.e. negative number or non-number values. The inputted value is there added or subtracted
        from the amount in the balance. If more money is to be withdrawn from an account than the account has stored
        it won't withdraw any money.
        :return:
        """
        try:
            amount = self.amount_input_accounts.text().strip()
            if amount == '':
                raise TypeError
            amount = eval(amount)
            if amount >= 0:
                if self.deposit_radio.isChecked():
                    new_total = self.__profile_info[self.current_account][2] + amount
                    self.__profile_info[self.current_account][2] = new_total
                    Logic.__profiles[self.__login_profile][self.__profile_info[self.current_account][0]][self.__profile_info[self.current_account][1]] = new_total
                elif self.withdraw_radio.isChecked():
                    if self.__profile_info[self.current_account][2] - amount < 0:
                        raise ValueError
                    else:
                        new_total = self.__profile_info[self.current_account][2] - amount
                        self.__profile_info[self.current_account][2] = new_total
                        Logic.__profiles[self.__login_profile][self.__profile_info[self.current_account][0]][self.__profile_info[self.current_account][1]] = new_total
                self.ui_update()
            else:
                raise TypeError
        except (TypeError, NameError):
            self.amount_input_accounts.setPlaceholderText('Positive # Only')
            self.amount_input_accounts.clear()
        except ValueError:
            self.amount_input_accounts.setPlaceholderText('Amount entered is to large to withdraw')
            self.amount_input_accounts.clear()
        finally:
            self.set_account_info()
