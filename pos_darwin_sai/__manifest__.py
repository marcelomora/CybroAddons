{
    "name": "Pos Darwin Sympthon and Active Ingredient",
    "summary": "Add Symptoms and active ingredients to products, so searches can be made by such fields",
    "version": "12.1.0.0",
    "category": "Inventory",
    "website": "accioma.com",
    "author": "Marcelo Mora <marcelo.mora@accioma.com>",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/sai_views.xml",
        "views/product_template_views.xml",
    ]
}
