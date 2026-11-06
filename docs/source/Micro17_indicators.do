gen		receive_wages = 1 if fin34a == 1  & account_fin != .					// received payments into an account
replace		receive_wages = 1 if fin34c2 == 1 & account_fin != .				// received payments into a card
replace	receive_wages = 1 if fin34b == 1 & account_mob != .						// received payments into a mobile
replace receive_wages = 2 if fin34c1 == 1 & receive_wages!=1					// received payments in cash only
replace receive_wages = 3 if fin32 == 1  & receive_wages!=1 & receive_wages!=2	// received payments using other methods
replace receive_wages = 4 if fin32 == 2 										// did not receive payments
replace receive_wages = 5 if fin32 == 3 | fin32 == 4							// dk/ref
lab var receive_wages "Payments: wage payments"
lab def receive_wages 1 "into an account" 2 "in cash" 3 "using other methods only" 4 "did not receive payments" 5 "(dk)/ref", replace
lab val receive_wages receive_wages


gen		receive_transfers = 1 if fin37 == 1 & fin39a == 1  & account_fin != .						// received payments into an account 
replace receive_transfers = 1 if fin37 == 1 & fin39c2 == 1 & account_fin != .						// received payments into an card
replace	receive_transfers  = 1 if fin37 == 1 & fin39b == 1 & account_mob != .						// received payments into a mobile
replace receive_transfers = 2 if fin37 == 1 & fin39c1 == 1 & receive_transfers!=1					// received payments in cash only
replace receive_transfers = 3 if fin37 == 1  & receive_transfers!=1 & receive_transfers!= 2			// received payments using other methods
replace receive_transfers = 4 if fin37 == 2 														// did not receive payments
replace receive_transfers = 5 if fin37 == 3 | fin37 == 4											// dk/ref
lab var receive_transfers "Payments: government transfers"
lab def receive_transfers 1 "into an account" 2 "in cash" 3 "using other methods only" 4 "did not receive payments" 5 "(dk)/ref", replace
lab val receive_transfers pay_received

gen		receive_pension = 1 if fin38 == 1 & fin39a == 1  & account_fin != .								// received payments into an account 
replace receive_pension = 1 if fin38 == 1 & fin39c2 == 1 & account_fin != .								// received payments into an card
replace	receive_pension  = 1 if fin38 == 1 & fin39b == 1 & account_mob != .								// received payments into a mobile
replace receive_pension = 2 if fin38 == 1 & fin39c1 == 1 & receive_pension!=1							// received payments in cash only
replace receive_pension = 3 if fin38 == 1  & receive_pension!=1 & receive_pension!= 2					// received payments using other methods
replace receive_pension = 4 if fin38 == 2 																// did not receive payments
replace receive_pension = 5 if fin38 == 3 | fin38 == 4													// dk/ref
lab var receive_pension "Payments: government pension"
lab def receive_pension 1 "into an account" 2 "in cash" 3 "using other methods only" 4 "did not receive payments" 5 "(dk)/ref", replace
lab val receive_pension pay_received


gen		receive_agriculture = 1 if fin43a == 1  & account_fin != .										// received payments into an account 
replace receive_agriculture = 1 if fin43c2 == 1 & account_fin != .										// received payments into an card
replace	receive_agriculture = 1 if fin43b == 1 & account_mob != .										// received payments into a mobile
replace receive_agriculture = 2 if fin43c1 == 1 & receive_agriculture!=1								// received payments in cash only
replace receive_agriculture = 3 if fin42 == 1  & receive_agriculture != 1 & receive_agriculture != 2	// received payments using other methods
replace receive_agriculture = 4 if fin42 == 2 															// did not receive payments
replace receive_agriculture = 5 if fin42 == 3 | fin42 == 4												// dk/ref
lab var receive_agriculture "Payments: selling agricultural goods"
lab def receive_agriculture 1 "into an account" 2 "in cash" 3 "using other methods only" 4 "did not receive payments" 5 "(dk)/ref", replace
lab val receive_agriculture pay_received

gen		pay_utilities = 1 if fin31a == 1	& account_fin != .											// made payments from an account
replace pay_utilities = 1 if fin31b == 1	& account_mob != .											// Add from a mobile 
replace pay_utilities = 2 if fin31c == 1 & pay_utilities!=1												// made payments in cash only
replace pay_utilities = 3 if fin30 == 1  & pay_utilities!=1 & pay_utilities!= 2							// made payments payments using other methods
replace pay_utilities = 4 if fin30 == 2 																// did not make payments
replace pay_utilities = 5 if fin30 == 3 | fin30 == 4													// dk/ref
lab var pay_utilities "Payments: utility bills"
lab def pay_utilities 1 "into an account" 2 "in cash" 3 "using other methods only" 4 "did not receive payments" 5 "(dk)/ref", replace
lab val pay_utilities pay_made


gen		remittances = 1 if d17==1  &  fin26 == 1 & fin27a == 1 & account_fin == 1								// acc fin: sent
replace remittances = 1 if d17==1  &  fin26 == 1 & fin27b == 1 & account_mob == 1								// acc mob: sent
replace remittances = 1 if d17==1  &  fin28 == 1 & fin29a == 1 & account_fin == 1								// acc fin: received
replace remittances = 1 if d17==1  &  fin28 == 1 & fin29b == 1 & account_mob == 1								// acc mob: received
replace	remittances = 2 if  fin26 == 1 & remittances != 1	 & account == 1 & (fin27a == 1 & account_fin != 1)	// otc fin: sent
replace remittances = 2 if fin26 == 1 & remittances != 1	 & account == 1 & (fin27b == 1 & account_mob != 1)	// otc mob: sent
replace	remittances = 2 if fin26 == 1 & remittances != 1	 & account != 1 & (fin27a == 1) 					// otc fin: sent
replace remittances = 2 if fin26 == 1 & remittances != 1	 & account != 1 & (fin27b == 1) 					// otc mob: sent
replace remittances = 2 if fin28 == 1 & remittances != 1	& account == 1 & (fin29a == 1 & account_fin  != 1)	// otc fin: received
replace remittances = 2 if fin28 == 1 & remittances != 1	& account == 1 & (fin29b == 1 & account_mob != 1)	// otc mob: received
replace remittances = 2 if fin28 == 1 & remittances != 1	& account != 1 & (fin29a == 1) 						// otc fin: received
replace remittances = 2 if  fin28 == 1 & remittances != 1	& account != 1 & (fin29b == 1)						// otc mob: received
replace remittances = 2 if fin27c2==1 & remittances != 1														// otc mto: sent
replace remittances = 2 if fin29c2==1 & remittances != 1														// otc mto: received
replace remittances = 3 if fin27c1==1 & remittances != 1 & remittances != 2										// in cash only: sent
replace remittances = 3 if fin29c1==1 & remittances != 1 & remittances != 2										// in cash only: received
replace remittances = 4 if (fin26==1 | fin28==1) & remittances != 1 & remittances != 2 & remittances != 3		// using other methods
replace remittances = 5 if (fin26==2 & fin28==2)																// did not send/receive
replace remittances = 6 if (fin26!=. & fin28!=.) & remittances != 1 & remittances != 2 & remittances != 3 & remittances != 4 & remittances != 5 // dk/ref 
lab var remittances "Domestic remittances"
lab def remittances 1 "into an account" 2 "using OTC" 3 "in cash" 4 "using other methods" 5 "did not send or receive" 6 "(dk)/ref", replace
lab val remittances remittances
