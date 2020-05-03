from StreamerTests.event_hubs_keys_hidden import conn_str, checkpoint_conn_str, checkpoint_container_name, event_hub_name
import asyncio
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData


async def on_event(partition_context, event):
    # Print the event data.
    print("Received the event: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'), partition_context.partition_id))

    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)


async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    checkpoint_store = BlobCheckpointStore.from_connection_string(checkpoint_conn_str, checkpoint_container_name)

    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string(conn_str, consumer_group="$Default", eventhub_name=event_hub_name, checkpoint_store=checkpoint_store)

    client_future = client.receive(on_event=on_event, starting_position=-1)
    print('client is listening')

    producer = EventHubProducerClient.from_connection_string(conn_str=conn_str, eventhub_name=event_hub_name)
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData('First event '))
        event_data_batch.add(EventData('Second event'))
        event_data_batch.add(EventData('Third event'))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)
        print('sent events')

    await client_future

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Run the main method.
    loop.run_until_complete(main())