def get_seasons_in_correct_format(start_year: int = 2000,
                                  end_year: int = 2024,
                                  format: str = "YYYY-YY"):
    years = []
    num_years = end_year - start_year

    if num_years < 0:
        raise ValueError("Your end_year is earlier than your start year.")

    if format == "YYYY-YY":
        current_year = start_year
        for _ in range(num_years):
            year_after = current_year + 1
            formatted_season = str(current_year) + "-" + str(year_after)[-2:]
            years.append(formatted_season)

            current_year += 1

    return years