if (typeof web3 !== 'undefined') {
    web3 = new Web3(web3.currentProvider);
} 
else {
    // set the provider you want from Web3.providers
    web3 = new Web3(new Web3.providers.HttpProvider("HTTP://127.0.0.1:7545"));
}

web3.eth.defaultAccount = web3.eth.accounts[0];

var StorageContract = new web3.eth.Contract([
	{
		"constant": true,
		"inputs": [],
		"name": "count_order",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_fromaddress",
				"type": "string"
			},
			{
				"name": "_toaddress",
				"type": "string"
			},
			{
				"name": "_orderid",
				"type": "uint256"
			},
			{
				"name": "_productid",
				"type": "uint256"
			},
			{
				"name": "_manufacturerid",
				"type": "uint256"
			},
			{
				"name": "_userid",
				"type": "uint256"
			},
			{
				"name": "_orderstatus",
				"type": "uint256"
			},
			{
				"name": "_logisticid",
				"type": "uint256"
			}
		],
		"name": "add_order",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_orderid",
				"type": "uint256"
			}
		],
		"name": "get_user_order_details",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_orderid",
				"type": "uint256"
			}
		],
		"name": "get_logistics_order_details",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "_orderid",
				"type": "uint256"
			}
		],
		"name": "get_manufacturer_order_details",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "string"
			},
			{
				"name": "",
				"type": "uint256"
			},
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "get_order_transactions",
		"outputs": [
			{
				"name": "",
				"type": "uint256[]"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
],'0xB0dd53446aE446A5D08B7CbD5de0341695644a36');