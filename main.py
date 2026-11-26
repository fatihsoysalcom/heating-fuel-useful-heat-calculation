def calculate_heating_metrics(
    monthly_fuel_consumption_m3: float,
    fuel_price_per_m3_tl: float,
    system_efficiency_percent: float,
    fuel_calorific_value_kwh_per_m3: float = 9.5  # Approximate for natural gas in Turkey
):
    """
    Calculates total energy input, useful heat output, energy lost, and estimated cost
    based on fuel consumption and heating system efficiency.

    Args:
        monthly_fuel_consumption_m3 (float): Total fuel consumed in cubic meters per month.
        fuel_price_per_m3_tl (float): Price of one cubic meter of fuel in Turkish Lira.
        system_efficiency_percent (float): Heating system efficiency as a percentage (e.g., 85 for 85%).
        fuel_calorific_value_kwh_per_m3 (float): Energy content of one cubic meter of fuel in kWh.
                                                 Default is for natural gas.

    Returns:
        dict: A dictionary containing calculated metrics.
    """

    # 1. Calculate total energy input from the consumed fuel
    # This is the total energy released by burning the fuel.
    total_energy_input_kwh = monthly_fuel_consumption_m3 * fuel_calorific_value_kwh_per_m3

    # 2. Calculate useful heat output
    # This is the actual heat delivered to the living space, considering system losses.
    # This directly addresses "Faydalı Isıyı Yakıt Tüketiminden Ayırmak" (Separating Useful Heat from Fuel Consumption).
    useful_heat_output_kwh = total_energy_input_kwh * (system_efficiency_percent / 100)

    # 3. Calculate energy lost due to system inefficiency
    # This represents the energy that is not converted into useful heat (e.g., flue gas losses, radiation losses).
    energy_lost_kwh = total_energy_input_kwh - useful_heat_output_kwh

    # 4. Calculate the estimated total cost based on fuel consumption
    estimated_total_cost_tl = monthly_fuel_consumption_m3 * fuel_price_per_m3_tl

    # 5. Calculate the effective cost per unit of useful heat
    # This shows how much you pay for each kWh of heat actually warming your home.
    effective_cost_per_useful_kwh_tl = estimated_total_cost_tl / useful_heat_output_kwh if useful_heat_output_kwh > 0 else 0

    return {
        "total_energy_input_kwh": total_energy_input_kwh,
        "useful_heat_output_kwh": useful_heat_output_kwh,
        "energy_lost_kwh": energy_lost_kwh,
        "estimated_total_cost_tl": estimated_total_cost_tl,
        "effective_cost_per_useful_kwh_tl": effective_cost_per_useful_kwh_tl
    }

if __name__ == "__main__":
    print("--- Heating Cost & Useful Heat Calculator ---")
    print("This calculator demonstrates how to separate useful heat from total fuel consumption,")
    print("highlighting the impact of heating system efficiency.")
    print("-" * 50)

    # Example parameters (can be modified by the user)
    # These values are illustrative and should be replaced with actual bill data.
    example_consumption_m3 = 150.0  # Example: 150 cubic meters of natural gas per month
    example_price_per_m3_tl = 6.5   # Example: 6.5 TL per cubic meter of natural gas
    example_system_efficiency_percent = 85.0 # Example: 85% efficiency for a typical boiler

    print(f"Input Parameters:")
    print(f"  Monthly Fuel Consumption: {example_consumption_m3:.1f} m³")
    print(f"  Fuel Price per m³: {example_price_per_m3_tl:.2f} TL")
    print(f"  Heating System Efficiency: {example_system_efficiency_percent:.1f}%")
    print("-" * 50)

    results = calculate_heating_metrics(
        monthly_fuel_consumption_m3=example_consumption_m3,
        fuel_price_per_m3_tl=example_price_per_m3_tl,
        system_efficiency_percent=example_system_efficiency_percent
    )

    print("Calculation Results:")
    print(f"  Total Energy Input from Fuel: {results['total_energy_input_kwh']:.2f} kWh")
    print(f"  Useful Heat Delivered to Home: {results['useful_heat_output_kwh']:.2f} kWh")
    print(f"  Energy Lost (due to inefficiency): {results['energy_lost_kwh']:.2f} kWh")
    print(f"  Estimated Total Fuel Cost: {results['estimated_total_cost_tl']:.2f} TL")
    print(f"  Effective Cost per Useful kWh: {results['effective_cost_per_useful_kwh_tl']:.2f} TL/kWh")
    print("-" * 50)

    # Demonstrate impact of different efficiency
    print("\n--- Impact of System Efficiency ---")
    print("Let's see how a less efficient system (e.g., 70%) affects useful heat and cost:")
    less_efficient_results = calculate_heating_metrics(
        monthly_fuel_consumption_m3=example_consumption_m3,
        fuel_price_per_m3_tl=example_price_per_m3_tl,
        system_efficiency_percent=70.0 # Lower efficiency
    )
    print(f"  For 70% Efficiency:")
    print(f"    Useful Heat Delivered: {less_efficient_results['useful_heat_output_kwh']:.2f} kWh")
    print(f"    Energy Lost: {less_efficient_results['energy_lost_kwh']:.2f} kWh")
    print(f"    Effective Cost per Useful kWh: {less_efficient_results['effective_cost_per_useful_kwh_tl']:.2f} TL/kWh")
    print("-" * 50)
