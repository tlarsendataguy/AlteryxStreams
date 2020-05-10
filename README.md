# AlteryxStreams

An experiment in streaming data into Alteryx

## Disclaimer

This and the related codebases contain experimental code to prove whether the idea works.  The code is ugly and may contain many unhandled edge cases.  Don't use in production.  If I were to someday put these tools into production, I would rebuild the codebases from the ground up using proper coding techniques.

## Related codebases

- [Golang webserver for Avocado API](https://github.com/tlarsen7572/Golang-Public/tree/master/alteryx_streams_server)
- [Avocado web GUI](https://github.com/tlarsen7572/alteryx_streams_avocado_gui)

## To install the Alteryx tools

1. Clone this repository to your local machine
2. Navigate to the repository root folder.
3. Run makeStreamerLinks.bat as an administrator.  This creates symbolic links in C:\ProgramData\Alteryx\Tools that point to the cloned repository.  This allows Alteryx to load the tools normally while at the same time allowing the code to remain packaged in the repository.
4. The streamer tools require 5 non-standard Python packages.  I installed them directly into Alteryx's Miniconda installation.  They are listed in the requirements.txt file in the root of the repository.


## To install and run the Avocado webserver example

1. Download and install [RabbitMQ](https://www.rabbitmq.com/) using standard ports.
2. Download [the Avocado webserver](https://github.com/tlarsen7572/AlteryxStreams/releases/download/v0.1/alteryx_streams_server.zip) and unzip to a folder of your choosing.
3. Run alteryx_streams_server.exe
4. Download [the Avocado workflow](https://github.com/tlarsen7572/AlteryxStreams/releases/download/v0.1/Streamer.RabbitMQ.Eats.Avocados.yxmd)
5. Run the Avocado workflow
6. Open your browser and navigate to http://localhost:53014
7. Type in any valid query and click 'Query Alteryx'.  The result should appear between the query and the button.  See the 'Things you should know about the Avocado query' section below.
8. Conquer the Avocado industry

## Things you should know about the Avocado query

* Because this is a proof-of-concept, I did not re-create all of the functions available in Alteryx.  The normal operators are available, as are the Min, Max, and POW functions.
* Function and field names are case sensitive (Min, not MIN, and POW, not pow)
* You can use `IF THEN ELSE ENDIF` and `IF THEN ELSEIF ELSE ENDIF` statements, just like in Alteryx.
* Use the `[Calc]` field to refer to the prior calculated value.

### Examples:

Calculate the total sales volume in the file:
```
[Calc] + [Total Volume]
```

Calculate the total sales value in the file:
```
[Calc] + ([Total Volume] * [AveragePrice])
```

Calculate the total sales value for 2018:
```
IF [year] = '2018' THEN [Calc] + ([Total Volume] * [AveragePrice]) ELSE [Calc] ENDIF
```

Calculate max price:
```
Max([Calc], [AveragePrice])
```
