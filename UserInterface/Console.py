from Service.ClientCardService import ClientCardService
from Service.DrugService import DrugService
from Service.RandomEntityGenerator import GenerateEntityService
from Service.TransactionService import TransactionService
from Service.cascade_deletionservice import CascadeDeletion
from Service.undo_redo_service import UndoRedoService


class Console:
    def __init__(self,
                 drug_service: DrugService,
                 client_card_service: ClientCardService,
                 transaction_service: TransactionService,
                 generator_service: GenerateEntityService,
                 cascade_deletion_service: CascadeDeletion,
                 undo_redo_service: UndoRedoService
                 ):
        self.drug_service = drug_service
        self.client_card_service = client_card_service
        self.transaction_service = transaction_service
        self.generator_service = generator_service
        self.cascade_deletion_service = cascade_deletion_service
        self.undo_redo_service = undo_redo_service

    @staticmethod
    def show_menu():
        print('============================================Menu============================================')
        print('add drug|client_card|transaction] '
              '- add transaction/client card/transaction.')
        print('update drug|client_card|transaction] '
              '- update transaction/client card/transaction.')
        print('delete drug|client_card|transaction] '
              '- delete transaction/client card/transaction.')
        print('show drugs|client cards|transactions] '
              '- show all transaction/client card/transaction.')
        print('genrand - Generate Random Entities for drugs')
        print('search drug - search full text in drugs')
        print('search client - search full text in client cards')
        print('interval - Show all transaction from a given interval')
        print('sorted - Show all drugs in descending order by numbers of sale')
        print('sale - Show all client cards in descending order by the value '
              'of the discount obtained')
        print('delete interval- Delete transaction from a given interval ')
        print('increase - increase the drugs that are lower than a val'
              'ue given with a given %')
        print('cascade - Deletes in cascade drugs/client card')
        print('Undo')
        print('Redo')
        print('x.Exit')
        print('===========================================================================================')
    def run_console(self):
        while True:
            self.show_menu()
            option = input("Choose an option : ")

            if option.casefold() == 'add drug':
                self.handle_add_drug()
            elif option.casefold() == 'show drugs':
                self.handle_show_all(self.drug_service.get_all())
            elif option.casefold() == 'add client card':
                self.handle_add_client_card()
            elif option.casefold() == 'show client cards':
                self.handle_show_all(self.client_card_service.get_all())
            elif option.casefold() == 'add transaction':
                self.handle_add_transaction()
            elif option.casefold() == 'show transactions':
                self.handle_show_all(self.transaction_service.get_all())
            elif option.casefold() == 'update drug':
                self.handle_update_drug()
            elif option.casefold() == 'update client_card':
                self.handle_update_client()
            elif option.casefold() == 'update transaction':
                self.handle_update_transaction()
            elif option.casefold() == 'genrand':
                self.handle_generate_entity()
            elif option.casefold() == 'delete drug':
                self.handle_delete_drug()
            elif option == 'delete client card ':
                self.handle_delete_client_card()
            elif option.casefold() == 'delete transaction':
                self.handle_delete_transaction()
            elif option.casefold() == 'search drug':
                self.handle_search_text_drug()
            elif option.casefold() == 'search client':
                self.handle_search_text_client()
            elif option.casefold() == 'interval':
                self.handle_interval()
            elif option.casefold() == 'sorted':
                self.handle_sorted_drugs()
            elif option.casefold() == 'sale':
                self.handle_descending_order()
            elif option.casefold() == 'delete interval':
                self.handle_delete_interval_transaction()
            elif option.casefold() == 'increase':
                self.handle_increase_price()
            elif option.casefold() == 'cascade':
                self.handle_delete_cascade()
            elif option.casefold() == 'Undo'.casefold():
                self.undo_redo_service.do_undo()
            elif option.casefold() == 'Redo'.casefold():
                self.undo_redo_service.do_redo()
            elif option.casefold() == 'x':
                break
            else:
                print("Invalid option! ")

            print("\n")

    def handle_add_drug(self):
        try:
            id_drug = input("Give drug id: ")
            drug_name = input("Give drug name: ")
            drug_producer = input("Give drug producer: ")
            drug_price = float(input("Give drug price: "))
            need_recipe = input("Need validation?(Yes/No): ")
            self.drug_service.add_drug(id_drug, drug_name,
                                       drug_producer, drug_price, need_recipe)
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    @staticmethod
    def handle_show_all(objects):
        for obj in objects:
            print(obj)

    def handle_add_client_card(self):
        try:
            id_client_card = input("Give client card id: ")
            client_name = input("Give client name: ")
            client_first_name = input("Give  client first name : ")
            client_cnp = input("Give CNP: ")
            client_birthdate = input("Give client birthdate: ")
            client_registration_date = input("Give client registration "
                                             " date: ")
            self.client_card_service.add_client_card(id_client_card,
                                                     client_name,
                                                     client_first_name,
                                                     client_cnp,
                                                     client_birthdate,
                                                     client_registration_date)
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    def handle_add_transaction(self):
        try:
            id_transaction = input("Give transaction id: ")
            drug_id = input("Give drug id: ")
            client_card_id = input("Give client card id: ")
            number_of_pieces = int(input("Give number of pieces: "))
            date_and_hour = input("Give date "
                                  "and hour: ")
            self.transaction_service.add_transaction(id_transaction, drug_id,
                                                     client_card_id,
                                                     number_of_pieces,
                                                     date_and_hour)
            sale = self.transaction_service.transaction_sale(client_card_id,
                                                             drug_id)
            if int(sale[1]) > 0:
                print(f"You've paid {sale[0]} with a discount of {sale[1]}%")
            else:
                print(f"You've paid {sale[0]}")

        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    def handle_generate_entity(self):
        n = int(input("How many entities you want to generate? "))
        self.generator_service.generate(n)

    def handle_search_text_drug(self):
        text = input("Give the text you want to search in drugs: ")
        print(self.drug_service.search(text))

    def handle_search_text_client(self):
        text = input("Give the text you want to search in client cards: ")
        print(self.client_card_service.search(text))

    def handle_update_drug(self):
        try:
            drug_id = input("Give the id of the drug you want to modify: ")
            drug_name = input("Give the new name:  ")
            drug_producer = input("Give the new producer: ")
            drug_price = float(input("Give the new price: "))
            need_recipe = input("Need recipe? [Yes/No]: ")
            self.drug_service.update_drug(drug_id, drug_name, drug_producer,
                                          drug_price, need_recipe)

            print("You have updated the drug with id {0}".format(drug_id))
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    def handle_update_client(self):
        try:
            id_client_card = input(
                "Give the id of the client card you want to modify: ")
            client_name = input("Give the new name:  ")
            client_first_name = input("Give the new first namer: ")
            client_cnp = input("Give the new CNP: ")
            client_birthdate = input(
                "Give the new birthdate in dd-mm-yyyy format: ")
            client_registration_d = input(
                "Give the new registration date in dd-mm-yyyy format: ")
            self.client_card_service.update_client_card(id_client_card,
                                                        client_name,
                                                        client_first_name,
                                                        client_cnp,
                                                        client_birthdate,
                                                        client_registration_d)

            print("You have updated the client card with id {0}".format(
                id_client_card))
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    def handle_update_transaction(self):
        try:
            id_transaction = input(
                "Give the id of the transaction you want to update:  ")
            drug_id = input("Give the id of the drug: ")
            id_client_card = input(
                "Give the id of the client card: ")
            number_of_pieces = int(input("Give the new price: "))
            date_and_hour = input(
                "Give the date and hour of the transaction in  dd-mm-yyyy "
                "HH:MM format")
            self.transaction_service.update_transaction(id_transaction,
                                                        drug_id,
                                                        id_client_card,
                                                        number_of_pieces,
                                                        date_and_hour)
            print(
                "You have updated the transaction with id {0}".format(drug_id))
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    def handle_delete_drug(self):
        try:
            id_drug = input("Give the drug you want to delete: ")
            self.drug_service.delete_drug(id_drug)
            print("You have deleted the drug with {0} id ".format(id_drug))
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    def handle_delete_client_card(self):
        try:
            id_cliend_card = input("Give the client card you want to delete: ")
            self.client_card_service.delete_client_card(id_cliend_card)
            print("You have deleted the client card with {0} id ".format(
                id_cliend_card))
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    def handle_delete_transaction(self):
        try:
            id_transaction = input("Give the drug you want to delete: ")
            self.transaction_service.delete_transaction(id_transaction)
            print("You have deleted the transaction with {0} id ".format(
                id_transaction))
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    def handle_interval(self):
        try:
            start_date = input(
                "Give the starting date with dd-mm-yyyy format : ")
            end_date = input("Give the final date dd-mm-yyyy format: ")
            result = self.transaction_service.transaction_interval(
                start_date, end_date)
            for i in result:
                print(i)
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    def handle_sorted_drugs(self):
        sort = self.transaction_service.descending_drugs()
        for i in sort:
            print(i)

    def handle_descending_order(self):
        self.transaction_service.descending_sales()

    def handle_delete_interval_transaction(self):
        try:
            start_date = input(
                "Give the starting date with dd-mm-yyyy format : ")
            end_date = input("Give the final date dd-mm-yyyy format: ")
            self.transaction_service.delete_transaction_interval(
                start_date, end_date)
            print("Transaction" +
                  start_date + "to " + " from to deleted successfully ")
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    def handle_increase_price(self):
        try:
            value = float(input(
                "Give the value : "))
            percentile = float(
                input("Give the percentile to increase the price : "))
            self.drug_service.increase_price(value, percentile)
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)

    def handle_delete_cascade(self):

        try:
            entity = input("Give type of entity : ")
            id_entity = input("Give the id of entity : ")
            self.cascade_deletion_service.delete(id_entity, entity)
        except ValueError as ve:
            print('Validation Error: ', ve)
        except KeyError as ke:
            print("ID Error: ", ke)
        except Exception as ex:
            print("Error: ", ex)
