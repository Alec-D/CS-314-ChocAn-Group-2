def check_state(state: str):
    state_list = ['AL', 'AK', 'AZ', 'AR', 'AS', 'CA', 'CO', 'CT', 'DE', 'DC', 
    'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC',
    'ND', 'MP', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'TT', 
    'UT', 'VT', 'VA', 'VI', 'WA', 'WV', 'WI', 'WY']
    if state in state_list:
        return True
    else:
        return False

def getInputNumberSafe(numOptions: int) -> int:
    while True:
        response = input("--> ")
        print("-------------------------------------------------")
        try:
            response = int(response)
            # if response in range(1, numOptions+1):
            if response >= 1 and response <= numOptions:
                return response
        except:
            pass
        print(f"Please enter a number between 1 and {numOptions}!")