from pyteal import *

handle_creation = Seq(
	App.globalPut(Bytes("dun"), Bytes("N/A")),
	App.globalPut(Bytes("dun_no"), Int(0)),
	Approve()
)

router = Router(
	"candidates",
	BareCallActions(
		no_op=OnCompleteAction.create_only(handle_creation),
	),
)

@router.method
def add_candidate(dun: abi.String, dun_no: abi.Uint64, state: abi.String):
	return Seq(
		App.globalPut(Bytes("dun"), dun.get()),
		App.globalPut(Bytes("dun_no"), dun_no.get()),
		App.globalPut(Bytes("state"), state.get()),
	)

@router.method
def read(*, output:abi.String):
	return output.set(App.globalGet(Bytes("dun")))

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