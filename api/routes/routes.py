from flask import jsonify, request
from models.child import Child
from models.person import Person
from main import db


class Routes:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        """Registra as rotas do aplicativo dentro da classe."""

        @self.app.route("/person", methods=["POST"])
        def create_person():
            try:
                data = request.get_json()
                # if not data.get('name'):
                #     return jsonify({"message": "Nome é obrigatório!"}), 400

                new_person = Person(name=data["name"])

                db.session.add(new_person)
                db.session.commit()

                children = new_person.get("child", [])
                for child_data in children:
                    child_name = child_data.get("name")
                    if child_name:
                        new_child = Child(name=child_name, person_id=new_person.id)
                        db.session.add(new_child)

                db.session.commit()

                return jsonify({
                    "message": "Pessoa criada com sucesso!",
                    "person": {
                        "id": new_person.id,
                        "name": new_person.name,
                        "children": [
                            {"id": child.id, "name": child.name} for child in new_person.children
                        ]
                    }
                }), 201
            except Exception as e:
                return jsonify({"message": f"Erro ao criar pessoa: {e}"}), 500

        @self.app.route("/child", methods=["POST"])
        def create_child():
            try:
                data = request.get_json()
                child_name = data.get("name", "")
                person_id = data.get("person_id")

                if not person_id:
                    return jsonify({"message": "Person ID é obrigatório!"}), 400

                new_child = Child(name=child_name, person_id=person_id)

                db.session.add(new_child)
                db.session.commit()

                return (
                    jsonify(
                        {
                            "message": "Filho criado com sucesso!",
                            "child": {"id": new_child.id, "name": new_child.name, "person_id": new_child.person_id},
                        }
                    ),
                    201,
                )
            except Exception as e:
                return jsonify({"message": f"Erro ao criar filho: {e}"}), 500

        @self.app.route("/person", methods=["GET"])
        def get_person():
            try:
                people = db.session.query(Person).all()
                people_data = []
                for person in people:
                    children = db.session.query(Child).filter(Child.person_id == person.id).all()
                    children_names = [child.name for child in children]
                    children_names = [{'name': child.name, 'id': child.id} for child in children]

                    people_data.append({"id": person.id, "name": person.name, "children": children_names})

                return jsonify(people_data), 200
            except Exception as e:
                return jsonify({"message": f"Erro ao buscar pessoas: {e}"}), 500

        @self.app.route("/person/<int:id>", methods=["PUT"])
        def edit_person(id):
            try:
                data = request.get_json()
                person = db.session.query(Person).filter_by(id=id).first()

                if not person:
                    return jsonify({"message": "Pessoa não encontrada!"}), 404

                new_name = data.get("name")
                if new_name:
                    person.name = new_name

                db.session.commit()

                return (
                    jsonify(
                        {"message": "Pessoa atualizada com sucesso!", "person": {"id": person.id, "name": person.name}}
                    ),
                    200,
                )
            except Exception as e:
                return jsonify({"message": f"Erro ao editar pessoa: {e}"}), 500

        @self.app.route("/person/<int:id>", methods=["DELETE"])
        def delete_person(id):
            try:
                person = db.session.query(Person).filter_by(id=id).first()

                if not person:
                    return jsonify({"message": "Pessoa não encontrada!"}), 404

                children = db.session.query(Child).filter_by(person_id=id).all()

                for child in children:
                    db.session.delete(child)

                db.session.delete(person)
                db.session.commit()

                return jsonify({"message": "Pessoa e filhos excluídos com sucesso!"}), 200
            except Exception as e:
                return jsonify({"message": f"Erro ao excluir pessoa e filhos: {e}"}), 500

        @self.app.route("/child/<int:child_id>", methods=["PUT"])
        def update_child(child_id):
            try:
                data = request.get_json()
                new_name = data.get("name")

                child = db.session.query(Child).get(child_id)
                if not child:
                    return jsonify({"message": "Filho não encontrado!"}), 404

                child.name = new_name
                db.session.commit()

                return (
                    jsonify(
                        {"message": "Filho atualizado com sucesso!", "child": {"id": child.id, "name": child.name}}
                    ),
                    200,
                )
            except Exception as e:
                return jsonify({"message": f"Erro ao atualizar filho: {e}"}), 500

        @self.app.route("/child/<int:child_id>", methods=["DELETE"])
        def delete_child(child_id):
            try:
                child = db.session.query(Child).get(child_id)
                if not child:
                    return jsonify({"message": "Filho não encontrado!"}), 404

                db.session.delete(child)
                db.session.commit()

                return jsonify({"message": "Filho removido com sucesso!"}), 200
            except Exception as e:
                return jsonify({"message": f"Erro ao remover filho: {e}"}), 500
