from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models import Person, Expense
from schemas.person_schema import PersonSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from schemas.expense_schema import ExpenseSchema
from marshmallow import ValidationError


expenseSchema=ExpenseSchema()

class Expensedetail(Resource):
    @jwt_required()
    def get(self, id):
        """get one"""
        user_id = get_jwt_identity()

        user_id = int(user_id)
        print("JWT identity:", get_jwt_identity())
        

        expense =Expense.query.filter_by(id=id, person_id=user_id).first()

        if not expense:
            return {"error": "Expense not found"}, 404

        return {
            "id": expense.id,
            "title": expense.title,
            "amount": float(expense.amount),
            "description": expense.description
        }
    @jwt_required()
    def patch(self, id):
    
        """update one"""
        user_id = get_jwt_identity()
        data=request.get_json()

        try:
            validated_data=expenseSchema.load(data)
        except ValidationError as error:
            return {'errors': error.messages}, 400

        expense=Expense.query.filter_by(id=id, person_id=user_id).first()

        if not expense:
            return {'error':'expense not found'}, 404

        expense.title = validated_data.get("title", expense.title)
        expense.amount = validated_data.get("amount", expense.amount)
        expense.description = validated_data.get("description", expense.description)

        db.session.commit()

        return {"message": "expense updated"}, 200

    @jwt_required()
    def delete(self, id):
        user_id = get_jwt_identity()

        expense=Expense.query.filter_by(id=id, person_id=user_id).first()

        if not expense:
            return {'error':'expense not found'}, 404

        db.session.delete(expense)
        db.session.commit()

        return {"message": "expense deleted"}, 200


