# Copyright (c) 2024, Chat Frappe and contributors
# For license information, please see license.txt

import frappe
import unittest


class TestArticle(unittest.TestCase):
	def setUp(self):
		# Create a test article
		self.article = frappe.get_doc({
			"doctype": "Article",
			"article_name": "Test Article",
			"author": "Test Author",
			"description": "This is a test article",
			"isbn": "1234567890",
			"status": "Available",
			"publisher": "Test Publisher"
		})

	def test_article_creation(self):
		# Test creating a new article
		self.article.insert()
		self.assertTrue(self.article.name)
		self.assertEqual(self.article.article_name, "Test Article")
		self.assertEqual(self.article.status, "Available")

	def test_article_validation(self):
		# Test validation for short ISBN
		self.article.isbn = "123"
		self.assertRaises(frappe.ValidationError, self.article.insert)

	def test_article_status_change(self):
		# Test changing article status
		self.article.insert()
		self.article.status = "Issued"
		self.article.save()
		self.assertEqual(self.article.status, "Issued")

	def test_article_required_fields(self):
		# Test that required fields are enforced
		article = frappe.get_doc({
			"doctype": "Article",
			# Missing required field article_name
		})
		self.assertRaises(frappe.ValidationError, article.insert)

	def tearDown(self):
		# Clean up test data
		if frappe.db.exists("Article", self.article.name):
			frappe.delete_doc("Article", self.article.name)
