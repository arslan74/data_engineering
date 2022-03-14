import faust
from taxi_rides import TaxiRide


app = faust.App('datatalksclub.stream.v2', broker='kafka://localhost:9092')

# two topic
topic = app.topic('datatalkclub.yellow_taxi_ride1.json', 'datatalkclub.yellow_taxi_ride2.json',value_type=TaxiRide)

@app.agent(topic)
async def start_reading(records):
    async for record in records:
        print(record)


if __name__ == '__main__':
    app.main()