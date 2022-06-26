from Domain.Drug import Drug


class DrugValidator:
    @staticmethod
    def validate(drug: Drug):
        valid_recipe = ['Yes', 'No']
        if drug.need_recipe not in valid_recipe:
            raise ValueError(f"The recipe validation need to be "
                             f"{valid_recipe}.")
