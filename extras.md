# Current TODOs

- Refactor code : horrible modularization right now
- CLI frontend for all the endpoints
- Web based frontend

# Future Plans

- Add more pipelines and test out various approaches

- Add feedback system and support ticket system to generate more question answer pairs and continually improve data corpus
  
  Question gets added to support ticket queue , moderator answers it , its then added to master.db and the other downstream databases specific to each pipeline ( could be shared ) is updated via callback functions

- Make a ELO scoring system for various pipelines based on the feedback system

# Test Curl Commands
```
curl -X GET -H "Content-Type: application/json" -d '{"user_query": "What is lightning layer", "history": "", "pipeline": "default_pipeline"}' http://127.0.0.1:8000/chat
```

```
curl -X POST -H "Content-Type: application/json" -d '{"question": "I''m new to crypto, and I need a wallet. What should I look for in a good crypto wallet?", "answer": "A crypto wallet is a digital wallet used to securely store, send, and receive cryptocurrencies like Bitcoin, Ethereum, and others. It contains a user''s private and public keys for accessing their crypto holdings."}' http://localhost:8000/db/add
```

```
curl -X POST -H "Content-Type: application/json" -d '{"question": "Can you explain what a zkRollup is and how it relates to Ethereum?", "answer": "A zkRollup (Zero-Knowledge Rollup) is a Layer 2 scaling solution for Ethereum that uses zero-knowledge proofs to compress and validate transactions off-chain before bundling them and submitting them to the main Ethereum chain."}' http://localhost:8000/db/add
```

```
curl -X POST -H "Content-Type: application/json" -d '{"question": "What''s an ERC-20 token, and why is it important on Ethereum?", "answer": "An ERC-20 token is a standard for creating and issuing fungible tokens (like cryptocurrencies or utility tokens) on the Ethereum blockchain, governed by a set of rules and guidelines."}' http://localhost:8000/db/add
```