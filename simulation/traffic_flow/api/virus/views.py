from fastapi import APIRouter, Body, Response
import io

from models.virus import VirusModel, virus_stackplot
import matplotlib.pyplot as plt


from .schemas import VirusParams


router = APIRouter()

@router.post("", name="virus-model")
async def get_virus_model(virus_params: VirusParams = Body(...)):

    model = VirusModel(virus_params.dict())
    results = model.run()

    fig, ax = plt.subplots()
    virus_stackplot(results.variables.VirusModel, ax)

    with io.BytesIO() as fig_bytes:
        fig.savefig(fig_bytes, format="png")
        fig_bytes.seek(0)
        response = Response(fig_bytes.getvalue(), media_type="image/png")
        plt.close()

    return response

