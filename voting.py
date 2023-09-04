from pyteal import *

handle_creation = Seq(
	App.globalPut(Bytes("count"), Int(0)),
	Approve()
)

router = Router(
	"testingg",
	BareCallActions(
		no_op=OnCompleteAction.create_only(handle_creation),
	),
)

@router.method
def increment():
	scratchCount = ScratchVar(TealType.uint64)
	return Seq(
		scratchCount.store(App.globalGet(Bytes("count"))),
		App.globalPut(Bytes("count"), scratchCount.load() + Int(1)),
	)

@router.method
def decrement():
	scratchCount = ScratchVar(TealType.uint64)
	return Seq(
		Assert(Global.group_size() == Int(1)),
		scratchCount.store(App.globalGet(Bytes("count"))),
		If(
			scratchCount.load() > Int(0),
			App.globalPut(Bytes("count"), scratchCount.load() - Int(1)),
		),	
	)

@router.method
def read_count(*, output:abi.Uint64):
	return output.set(App.globalGet(Bytes("count")))

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