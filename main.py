from ai_interface.modules.real_test_data_generator.RealTestDataGenerator import RealTestDataGenerator as RTDG

generator = RTDG()
response = generator.generate_test_addresses("openai", "address", 3, country="czech republic")
print("\n\n\n", response, "\n\n\n")


