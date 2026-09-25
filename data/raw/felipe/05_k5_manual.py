def nb_months(start_price_old, start_price_new, saving_per_month, percent_loss_by_month):

    old_car_price = start_price_old
    new_car_price = start_price_new

    months = 0
    total_savings = 0

    if start_price_old >= start_price_new:
        difference = start_price_old - start_price_new
        return [0, round(difference)]

    while True:

        months = months + 1

        # A cada dois meses a porcentagem aumenta
        if months % 2 == 0:
            percent_loss_by_month = percent_loss_by_month + 0.5

        # Calculando a perda do carro antigo
        old_loss = old_car_price * percent_loss_by_month / 100
        old_car_price = old_car_price - old_loss

        # Calculando a perda do carro novo
        new_loss = new_car_price * percent_loss_by_month / 100
        new_car_price = new_car_price - new_loss

        # Valor que foi guardado no mês
        total_savings = total_savings + saving_per_month

        # Verificar se já é possível comprar o carro
        current_money = old_car_price + total_savings

        if current_money >= new_car_price:
            # TODO: calcular o dinheiro que sobra
            pass

    return [months, round(leftover)]