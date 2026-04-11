class OrderModel {
  final int id;
  final String customerName;
  final String? customerPhone;
  final String deliveryAddress;
  final double totalAmount;
  final String paymentMethod;
  final String paymentStatus;
  final String deliveryStatus;
  final String kitchenStatus;
  final DateTime createdAt;
  final List<OrderItemModel> items;
  final int? riderId;

  OrderModel({
    required this.id,
    required this.customerName,
    this.customerPhone,
    required this.deliveryAddress,
    required this.totalAmount,
    required this.paymentMethod,
    required this.paymentStatus,
    required this.deliveryStatus,
    required this.kitchenStatus,
    required this.createdAt,
    required this.items,
    this.riderId,
  });

  factory OrderModel.fromJson(Map<String, dynamic> json) {
    return OrderModel(
      id: json['id'],
      customerName: json['customer_name'] ?? 'Unknown',
      customerPhone: json['customer_phone'],
      deliveryAddress: json['delivery_address'] ?? 'No address',
      totalAmount: (json['total_amount'] as num).toDouble(),
      paymentMethod: json['payment_method'] ?? 'CASH',
      paymentStatus: json['payment_status'] ?? 'UNPAID',
      deliveryStatus: json['delivery_status'] ?? 'WAITING',
      kitchenStatus: json['status'] ?? 'PENDING',
      createdAt: DateTime.parse(json['created_at']),
      items: (json['items'] as List)
          .map((i) => OrderItemModel.fromJson(i))
          .toList(),
      riderId: json['rider_id'],
    );
  }
}

class OrderItemModel {
  final String name;
  final int quantity;
  final double price;

  OrderItemModel({
    required this.name,
    required this.quantity,
    required this.price,
  });

  factory OrderItemModel.fromJson(Map<String, dynamic> json) {
    return OrderItemModel(
      name: json['name'],
      quantity: json['quantity'],
      price: (json['price'] as num).toDouble(),
    );
  }
}
