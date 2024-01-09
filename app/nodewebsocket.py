from substrateinterface import SubstrateInterface, Keypair, KeypairType
from substrateinterface.exceptions import SubstrateRequestException


substrate = SubstrateInterface(
    url="ws://127.0.0.1:9944",
    ss58_format=42,
    type_registry_preset='substrate-node-template'
)


keypair = Keypair.create_from_uri('//Alice')


def call_extrinsic_add_wavefunction(wavefunction_json_s):
    call = substrate.compose_call(
        call_module='WavefunctionModule',
        call_function='add_wavefunction',
        call_params={
            'thefunction': wavefunction_json_s,
        }
    )

    extrinsic = substrate.create_signed_extrinsic(call=call, keypair=keypair)
    
    try:
        receipt = substrate.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        print("Extrinsic '{}' sent and included in block '{}'".format(receipt.extrinsic_hash, receipt.block_hash))

    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))

