def nb_months(start_price_old, start_price_new, saving_per_month, percent_loss_by_month):
    if start_price_old >= start_price_new:
        return [0, round(start_price_old - start_price_new)]
    
    months = 0
    savings = 0
    current_old = start_price_old
    current_new = start_price_new
    
    while current_old + savings < current_new:
        months += 1
        
        # O aumento de 0.5 na perda ocorre nos meses 2, 4, 6...
        if months % 2 == 0:
            percent_loss_by_month += 0.5
            
        current_old -= current_old * (percent_loss_by_month / 100)
        current_new -= current_new * (percent_loss_by_month / 100)
        savings += saving_per_month
        
    leftover = (current_old + savings) - current_new
    return [months, round(leftover)]
