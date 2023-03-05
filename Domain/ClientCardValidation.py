import datetime

from Domain.ClientCard import ClientCard


class ClientCardValidation:
    @staticmethod
    def validate(client_card: ClientCard):
        """
        Validates a client card dates.
        :param client_card: Client card to be validated.
        :return: raises ValueError if the dates are invalid.
        """
        try:
            date_format = "%d-%m-%Y"
            datetime.datetime.strptime(client_card.client_birthdate,
                                       date_format)
            datetime.datetime.strptime(client_card.client_registration_date,
                                       date_format)
        except ValueError:
            raise ValueError("Date time format is invalid. ")
