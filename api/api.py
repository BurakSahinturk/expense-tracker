from fastapi import FastAPI, Depends, HTTPException
from datetime import date as Date
from pydantic import BaseModel, PositiveFloat
from expense import Expense

from api.dependencies import get_expense_service
from expense_service import ExpenseService
from exceptions import ExpenseNotFoundError, InvalidExpenseDataError, InvalidExpenseDescriptionError, InvalidCategoryError, InvalidDateError
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello world!"}

@app.get("/health")
def health():
    return {"status": "ok"}

class ExpenseCreateDTO(BaseModel):
    amount: float
    category: str
    description: str
    date: Date | None = None

@app.post("/expenses")
def create_expense(
    dto: ExpenseCreateDTO,
    service: ExpenseService = Depends(get_expense_service)
):
    new_expense_id = service.add_expense(
        dto.amount,
        dto.category,
        dto.description,
        dto.date
    )
    return {"id": new_expense_id}

@app.get("/expenses")
def list_expenses(service: ExpenseService = Depends(get_expense_service)):
    expenses: list[Expense] = service.list_expenses()
    return [expense.to_dict() for expense in expenses]

@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int, service: ExpenseService = Depends(get_expense_service)):
    try:
        expense = service.get_expense(expense_id)
        return expense.to_dict()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    
class ExpensePatchDTO(BaseModel):
    amount: PositiveFloat | None = None
    category: str | None = None
    description: str | None = None
    date: Date | None = None

@app.patch("/expenses/{expense_id}")
def patch_expense(
    expense_id: int,
    dto: ExpensePatchDTO,
    service: ExpenseService = Depends(get_expense_service),
):
    if dto.amount is None and dto.category is None and dto.description is None and dto.date is None:
        raise HTTPException(status_code=400, detail="Found nothing to update")
    
    try:
        service.apply_patch(expense_id, dto)
        updated_expense = service.get_expense(expense_id)
        return updated_expense.to_dict()
    except ExpenseNotFoundError:
        raise HTTPException(status_code=404, detail="Expense not found")
    except InvalidExpenseDataError:
        raise HTTPException(status_code=400, detail="Invalid Amount")
    except InvalidCategoryError:
        raise HTTPException(status_code=400, detail="Invalid Category")
    except InvalidExpenseDescriptionError:
        raise HTTPException(status_code=400, detail="Invalid Description")
    except InvalidDateError:
        raise HTTPException(status_code=400, detail="Invalid Date")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))