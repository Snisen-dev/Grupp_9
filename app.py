from fastapi import FastAPI

app = FastAPI()

class AllaRum:
    # __init__ ?
    rum_id: int
    alla_rum = [None]
    bokade_rum = [None]
    obokade_rum = [None]
    bokat: bool = False

    class BokadeRum:
        bokat: bool = True
        bokade_rum = [None]

    class ObokadeRum:
        bokat: bool = False


@app.get("/")
async def root():
    return {'Message ' : 'Välkommen till Grupp 9:s bokingssystem'}

@app.get("/rum")
async def kolla_bokingar():
    return AllaRum.alla_rum


@app.get("/rum/bokat")
async def bokade_rum():
    return AllaRum.bokade_rum

@app.get("rum/obokade")
async def obokade_rum():
    return AllaRum.obokade_rum

@app.post("/boka")
async def ny_bokning():
    nuvarande_rum = AllaRum.rum_id
    if nuvarande_rum(AllaRum.bokat) == False:
        print('Rum bokat')
