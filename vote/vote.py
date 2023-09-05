from pyteal import *
from algosdk import encoding

k_vote_id_dun = Bytes("vote_id_dun")
k_vote_id_par = Bytes("vote_id_par")

router = Router(
	"voting_area_initialisation",
	BareCallActions(
		no_op=OnCompleteAction.create_only(Approve()),
		opt_in=OnCompleteAction.call_only(Approve())
	)
)

@router.method
def vote(id: abi.Uint8, voting_key: abi.Address):
	is_valid_id = And(
		id.get() > Int(0),
		id.get() < Int(8)
	)
	# Fak, how to solve??
	lol = encoding.decode_address(Addr(Txn.sender()))
	#is_valid_key = voting_key == Txn.sender()
	check = And(
		is_valid_id,
		#is_valid_key
	)
	ret = If(
		check,
		App.localPut(Txn.sender(), k_vote_id_dun, id.get())
	)
	return ret

@router.method
def read_vote(*, output: abi.Uint8):
	ret = App.localGet(Txn.sender(), k_vote_id_dun)
	return output.set(ret)

if __name__ == "__main__":
	import os
	import json

	path = os.path.dirname(os.path.abspath(__file__))
	approval, clear, contract = router.compile_program(version=8)

	# Write out the approval & clear program
	with open(os.path.join(path, "artifacts/approval.teal"), "w") as f:
		f.write(approval)

	with open(os.path.join(path, "artifacts/clear.teal"), "w") as f:
		f.write(clear)

	# Dump out the contract as JSON to be used by any SDKs
	with open(os.path.join(path, "artifacts/contract.json"), "w") as f:
		f.write(json.dumps(contract.dictify(), indent=2))