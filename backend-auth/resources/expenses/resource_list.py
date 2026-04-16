from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models import Person, Expense
from schemas.person_schema import PersonSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.expense_schema import ExpenseSchema
from marshmallow import ValidationError


expenseSchema=ExpenseSchema()


#get all
class Access_res(Resource):
    @jwt_required()
    def get(self):
        """getting all expenses of logged in user"""
        user_id = get_jwt_identity()

        page=request.args.get('page', 1)
        per_page=request.args.get('per_page', 10)
        # we create a plan to fetch and add more intructions on the base obj n if we use .all fetches all and crashes as data is alredy there
        BaseQuery = Expense.query.filter_by(person_id=user_id)

        # create a pagination objecst with built in attributes like has_prev, has_next , items, pages (errior_out is used to return [] if no data)
        paginated = BaseQuery.paginate(page=page, per_page=per_page, error_out=False)

        expenses=paginated.items

        exp={
        "items":[
        {
            "id":e.id,
            "title": e.title,
            "amount": float(e.amount),
            "description": e.description
        } 
        for e in expenses], 
        "pagination": {
                "page": paginated.page,
                "per_page": paginated.per_page,
                "total_pages": paginated.pages,
                "total_items": paginated.total,
                "has_next": paginated.has_next,
                "has_prev": paginated.has_prev
            }
        }
        
        return exp, 200
    
    @jwt_required()
    def post(self):
        """add data to database"""
        user_id = get_jwt_identity()
        data=request.get_json()

        try:
            validated_data=expenseSchema.load(data)
        except ValidationError as error:
            return {'errors': error.messages}, 400

        print(validated_data)

        try:
            new_expense=Expense(
                title=validated_data.get("title"),
                amount=validated_data.get("amount"),
                description=validated_data.get("description"),
                person_id=user_id 
            )

            db.session.add(new_expense)
            db.session.commit()

            return {'messsge':'expense created successfully!'}
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500



