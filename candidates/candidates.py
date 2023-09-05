from pyteal import *

k_name = Bytes("candidate_name")
k_dun_no = Bytes("candidate_dun_no")

#handle_creation = Seq(
#	App.globalPut(Bytes("dun"), Bytes("NULL")),
#	App.globalPut(Bytes("dun_no"), Int(0)),
#	App.globalPut(Bytes("state"), Bytes("NULL_STATE")),
#	Approve()
#)

router = Router(
	"candidates",
	BareCallActions(
		no_op=OnCompleteAction.create_only(Approve()),
		opt_in=OnCompleteAction.call_only(Approve()),
	),
)

@router.method
def candidates_info_to_contract(name: abi.String, dun_no: abi.Uint8):
	return Seq(
	 	App.localPut(Txn.sender(), k_name, name.get()),
		App.localPut(Txn.sender(), k_dun_no, dun_no.get()),
	)

@router.method
def read_candidate_name(*, output: abi.String):
	return output.set(App.localGet(Txn.sender(), Bytes("candidate_name")))

@router.method
def read_dun_no(*, output: abi.Uint8):
	return output.set(App.localGet(Txn.sender(), Bytes("candidate_dun_no")))

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